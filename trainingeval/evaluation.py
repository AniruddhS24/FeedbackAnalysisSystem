from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
import argparse
import yaml
from data.dataprocessing import *
from models.featurescorer import *
from models.extractor import *
from models.predictor import *
sys.path.pop(0)

def _parse_args():
    with open(r'trainingeval/config.yaml') as f:
        trainingconfig = yaml.full_load(f)

    parser = argparse.ArgumentParser(description='EVALUATOR')
    parser.add_argument('--model', type=str, help='model to evaluate: (' + ', '.join(trainingconfig.keys()) + ')')
    parser.add_argument('--savepath', type=str, default='saved/nonamemodel.pt',
                        help='file path of saved model, set up as saved/[filename].pt')
    parser.add_argument('--dataset', type=str, default='YELP',
                        help='dev dataset to use')
    parser.add_argument('--num_samples', type=int, default=1000, help='number of dev samples')
    parser.add_argument('--auxmodelsavepath', type=str, default=None, help='auxiliary model param file save path (ext or supp)')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = _parse_args()

    if torch.cuda.is_available():
        device = torch.device("cuda:0")
        print("Running on the GPU")
    else:
        device = torch.device("cpu")
        print("Running on the CPU")

    modelname = args.model
    datasetname = args.dataset
    savefile = args.savepath
    num_samples = args.num_samples
    auxpath = args.auxmodelsavepath

    if modelname == 'suppmodel':
        train_x, train_y, dev_x, dev_y = read_dataset(datasetname, num_samples)
        model = FeatureImportanceScorer(model_file_path=savefile)
        evaluate_supp_model(model.net, model.tokenizer, dev_x, dev_y, device=device)
    else:
        raise Exception("Model evaluation not supported yet")