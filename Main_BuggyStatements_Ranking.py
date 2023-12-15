from extra_project_information import uncertain_inference
from ranking import RankingManager
from ranking.Keywords import *
from util.FileManager import join_path
from ranking.MultipleBugsManager import multiple_bugs_ranking
from ranking.Spectrum_Expression import JACCARD, SORENSEN_DICE, TARANTULA, OCHIAI, OP2, BARINEL, DSTAR, ROGERS_TANIMOTO, \
    AMPLE, \
    SIMPLE_MATCHING, RUSSELL_RAO, COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2, WONG1, SOKAL, DICE, HUMANN, ZOLTAR, \
    WONG2, ROGOT2, EUCLID, HAMMING, FLEISS, ANDERBERG, KULCZYNSKI2, HARMONIC_MEAN, GOODMAN



if __name__ == "__main__":
    # parameter configuration
    system_name = "BankAccountTP"
    buggy_systems_folder = "/home/whn/Desktop/BankAccountTP/4wise-BankAccountTP-1BUG-Full"
    sbfl_metrics = [TARANTULA, OCHIAI, OP2, BARINEL, DSTAR,
                    RUSSELL_RAO, SIMPLE_MATCHING, ROGERS_TANIMOTO, AMPLE, JACCARD,
                    COHEN, SCOTT, ROGOT1, GEOMETRIC_MEAN, M2,
                    WONG1, SOKAL, SORENSEN_DICE, DICE, HUMANN,
                    WONG2, EUCLID, ZOLTAR,
                    ROGOT2, HAMMING, FLEISS, ANDERBERG,
                    GOODMAN, HARMONIC_MEAN, KULCZYNSKI2]
    normalization = NORMALIZATION_ENABLE
    aggregation = AGGREGATION_ARITHMETIC_MEAN
    w = 0.5

    #first part
    uncertain_inference(buggy_systems_folder)

    multiple_bugs_ranking(system_name=system_name, buggy_systems_folder= buggy_systems_folder, sbfl_metrics=sbfl_metrics,
                          alpha=w, normalization=normalization, aggregation=aggregation)
