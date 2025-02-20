# 必要なパッケージをインストール（最初の1回のみ）
install.packages("SMARTTR")
install.packages("magrittr")
install.packages("dplyr")
install.packages("/private/var/folders/lx/yxlnvzs96291fgg1fvcnkqf80000gn/T/RtmpPYRBfK/downloaded_packages/SMARTTR_1.0.1.tar.gz", repos = NULL, type = "source")
library(SMARTTR)
library(magrittr)
library(dplyr)

  
opioid <- experiment(experiment_name = "opioid",
                         channels = "cfos",       # If you have more than one channel to import, set this to a character vector, e.g. c("cfos", "eyfp")
                         output_path = "/Users/saccyann/Documents/Sakura_networkanalysis/retry") #Set this to a path location where you want your figures/analysis output to save, e.g. "P:\\DENNYLABV\\Michelle_Jin\\experiment\\folder"
# output_path = tempdir()) #Set this to a path location where you want your figures/analysis output to save, e.g. "P:\\DENNYLABV\\Michelle_Jin\\experiment\\folder"
print(opioid)

opioid <- import_mapped_datasets(opioid, 
                                     normalized_count_paths = "/Users/saccyann/Documents/Sakura_networkanalysis/SMARTTR/cleaned_countdata_wobg_woco.csv",
                                     show_col_types = FALSE)
print(opioid)

head(SMARTTR::ontology.unified)

ontology <- "unified"   # Set to "allen" if you are using the allen ontology
#checking cfos ...が終わらないので一旦飛ばす。remote desktopでも。データセットの問題っぽい
#opioid <- check_ontology_coding(opioid, ontology = ontology)

# RDataファイルをロード（オブジェクト名はロード後に確認）
load("/Users/saccyann/Documents/Sakura_networkanalysis/SMARTTR/rejected_acronyms.RData")
opioid <- filter_regions(opioid, 
                             base_regions =  curated_acronyms,
                             ontology = ontology)

opioid <- exclude_redundant_regions(opioid, ontology = ontology)

# simplify the acronyms by the keywords and recalculate the normalized counts
#削るところを最小にした
simplify_keywords <-c("interfascicular part")
opioid <- simplify_cell_count(opioid, ontology = ontology, simplify_keywords = simplify_keywords, dont_fold = "")
exclusion_acronyms <- c("drt")
opioid <- exclude_by_acronym(opioid, acronyms = exclusion_acronyms, ontology = ontology)
keywords_exclude <- c("nerve", "tract", "pineal gland", "   Area subpostrema")
opioid <-  exclude_by_keyword(opioid, keywords = keywords_exclude)

#thresh <- 1
#opioid$combined_normalized_counts$cfos <- opioid$combined_normalized_counts$cfos %>% dplyr::filter(counts >= thresh)

opioid <- find_outlier_counts(opioid, by = c("group"), n_sd = 2, remove = TRUE, log = TRUE)

opioid <- enough_mice_per_group(opioid, by = c("group"), min_n = 4, remove = TRUE, log = TRUE)

save(opioid, file = "/Users/saccyann/Documents/Sakura_networkanalysis/SMARTTR/opioid_labdata_new.RData")


save_experiment(opioid, timestamp = TRUE)
print("success")

#githubでバージョン管理
