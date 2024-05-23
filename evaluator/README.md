# CODA2022 Evaluator

This directory contains the official evaluation code for [ECCV 2022 Workshop SSLAD Track 3 - Corner Case Detection](https://codalab.lisn.upsaclay.fr/competitions/6639).



## Usage

1. Install dependency.

   ```
   pip install pycocotools
   ```

2. Save your prediction file in the `prediction` directory. Make sure your prediction is saved in `json` files, and all the `json` files in the `prediction` directory belong to a single model.

3. Run the following script, and your evaluation results will be saved in `ans/scores.txt`.

   ```bash
   # For val
   python evaluate_val.py prediction/ ans/
   
   # For test
   python evaluate_test.py prediction/ ans/
   ```

   

