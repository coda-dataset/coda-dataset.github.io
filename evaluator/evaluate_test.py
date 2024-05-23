#!/usr/bin/env python
import copy, sys, os, os.path, json
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


def main():
  input_dir = sys.argv[1]
  output_dir = sys.argv[2]

  submit_dir = input_dir
  truth_dir = "data"

  if not os.path.isdir(submit_dir):
  	print ("%s doesn't exist" % submit_dir)

  results_shown = {}
  if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
      if not os.path.exists(output_dir):
          os.makedirs(output_dir)
      ######################################################################## get inference data
      submission_list = os.listdir(submit_dir)
      sub_all = []
      for submission in submission_list:
        if ".json" in submission:
          sub_part = json.load(open(os.path.join(submit_dir,submission) ,"r"))
          sub_all = sub_all + sub_part

      if len(sub_all) == 0:
        print("Error: No annotations found!")
        return

      print("The submission results get total %s annotations!" % (len(sub_all)))

      ######################################################################## compute AP-common
      print('Computing AP-common')
      sub_common = [pred for pred in sub_all if 1 <= pred['category_id'] <= 7]
      if not sub_common:
        print("Error: No annotations for common categories found!")
        return

      gold_file = os.path.join(truth_dir, "instance_test_common.json")
      coco = COCO(gold_file)
      cocoGt = coco
      img_ids = coco.getImgIds()
      print("Evaluating bbox!")

      try:
        cocoDt = cocoGt.loadRes(sub_common)
      except IndexError as e:
        print_log(str(e), logger=logger, level=logging.ERROR)
        return

      iou_type = 'bbox'
      cocoEval = COCOeval(cocoGt, cocoDt, iou_type)
      cocoEval.params.imgIds = img_ids
      cocoEval.evaluate()
      cocoEval.accumulate()
      cocoEval.summarize()
      results_shown['AP-common'] = cocoEval.stats[0]
      print(f'AP-common: {results_shown["AP-common"]:0.2f}')

      ######################################################################## compute AP-agnostic & AR-agnostic
      print('Computing AP-agnostic & AR-agnostic')
      sub_agnostic = []
      for pred in sub_all:
          sub_agnostic.append(copy.deepcopy(pred))
          sub_agnostic[-1]['category_id'] = 1
      gold_file = os.path.join(truth_dir, "instance_test_agnostic.json")
      coco = COCO(gold_file)
      cocoGt = coco
      img_ids = coco.getImgIds()
      print("Evaluating bbox!")

      try:
        cocoDt = cocoGt.loadRes(sub_agnostic)
      except IndexError as e:
        print_log(str(e), logger=logger, level=logging.ERROR)
        return

      iou_type = 'bbox'
      cocoEval = COCOeval(cocoGt, cocoDt, iou_type)
      cocoEval.params.imgIds = img_ids
      cocoEval.evaluate()
      cocoEval.accumulate()
      cocoEval.summarize()
      results_shown['AP-agnostic'] = cocoEval.stats[0]
      print(f'AP-agnostic: {results_shown["AP-agnostic"]:0.2f}')
      results_shown['AR-agnostic'] = cocoEval.stats[8]
      print(f'AR-agnostic: {results_shown["AR-agnostic"]:0.2f}')

      ######################################################################## compute AR-agnostic-corner
      print('Computing AR-agnostic-corner')
      gold_file = os.path.join(truth_dir, "instance_test_agnostic_corner.json")
      coco = COCO(gold_file)
      cocoGt = coco
      img_ids = coco.getImgIds()
      print("Evaluating bbox!")

      try:
        cocoDt = cocoGt.loadRes(sub_agnostic)
      except IndexError as e:
        print_log(str(e), logger=logger, level=logging.ERROR)
        return

      iou_type = 'bbox'
      cocoEval = COCOeval(cocoGt, cocoDt, iou_type)
      cocoEval.params.imgIds = img_ids
      cocoEval.evaluate()
      cocoEval.accumulate()
      cocoEval.summarize()
      results_shown['AR-agnostic-corner'] = cocoEval.stats[8]
      print(f'AR-agnostic-corner: {results_shown["AR-agnostic-corner"]:0.2f}')

      ######################################################################## compute metric sum
      results_shown['Sum'] = sum(results_shown.values())
      print(f'Sum: {results_shown["Sum"]:0.2f}')

      ######################################################################## write back
      output_filename = os.path.join(output_dir, 'scores.txt')
      output_file = open(output_filename, 'w')
      output_file.write("%s: %s\n" % ("Sum", results_shown["Sum"]))
      for key, value in results_shown.items():
          if key != "Sum":
              output_file.write("%s: %s\n" % (key, value))
      output_file.close()
      print('\n' + "Done!")

if __name__ == '__main__':
    main()
