# =============================================================================
# Robyn MMM — Indian FMCG National Weekly
# =============================================================================

.libPaths(c("C:/Rlibs", .libPaths()))
suppressPackageStartupMessages({
  library(Robyn)
  library(reticulate)
  library(data.table)
  library(dplyr)
  library(ggplot2)
  library(jsonlite)
})

set.seed(42)
options(warn = -1)

python_exe <- "C:/Users/BIPLOB GON/.local/bin/python3.14.exe"
Sys.setenv(RETICULATE_PYTHON = python_exe)
reticulate::use_python(python_exe, required = FALSE)

dt <- fread("data/processed/mmm_national_weekly.csv")
dt[, date := as.Date(date)]
cat("Rows:", nrow(dt), "| Cols:", ncol(dt), "
")
cat("Date range:", format(min(dt$date)), "to", format(max(dt$date)), "
")

data("dt_prophet_holidays", package = "Robyn")

InputCollect <- robyn_inputs(
  dt_input          = dt,
  dt_holidays       = dt_prophet_holidays,
  date_var          = "date",
  dep_var           = "sales",
  dep_var_type      = "revenue",
  prophet_vars      = c("trend", "season", "holiday"),
  prophet_country   = "IN",
  context_vars      = c("cpi", "gdp_growth", "festival", "trade_spend"),
  paid_media_spends = c("tv", "youtube", "facebook", "instagram",
                        "print_media", "radio"),
  paid_media_vars   = c("tv", "youtube", "facebook", "instagram",
                        "print_media", "radio"),
  window_start      = "2022-07-04",
  window_end        = "2025-06-23",
  adstock           = "geometric"
)

hyperparameters <- list(
  tv_alphas          = c(0.5, 3.0),
  tv_gammas          = c(0.3, 1.0),
  tv_thetas          = c(0.50, 0.85),
  youtube_alphas     = c(0.5, 3.0),
  youtube_gammas     = c(0.3, 1.0),
  youtube_thetas     = c(0.20, 0.55),
  facebook_alphas    = c(0.5, 3.0),
  facebook_gammas    = c(0.3, 1.0),
  facebook_thetas    = c(0.15, 0.50),
  instagram_alphas   = c(0.5, 3.0),
  instagram_gammas   = c(0.3, 1.0),
  instagram_thetas   = c(0.10, 0.45),
  print_media_alphas = c(0.5, 3.0),
  print_media_gammas = c(0.3, 1.0),
  print_media_thetas = c(0.30, 0.65),
  radio_alphas       = c(0.5, 3.0),
  radio_gammas       = c(0.3, 1.0),
  radio_thetas       = c(0.25, 0.60),
  train_size         = c(0.5, 0.8)
)

InputCollect <- robyn_inputs(
  InputCollect    = InputCollect,
  hyperparameters = hyperparameters
)

cat("
=== Running Nevergrad (iterations=200, trials=1, cores=4) ===
")
OutputModels <- robyn_run(
  InputCollect = InputCollect,
  cores        = 4,
  iterations   = 200,
  trials       = 1,
  outputs      = FALSE
)
cat("=== Optimisation complete ===
")

plot_dir <- "outputs/figures/robyn"
dir.create(plot_dir, showWarnings = FALSE, recursive = TRUE)

OutputCollect <- robyn_outputs(
  InputCollect  = InputCollect,
  OutputModels  = OutputModels,
  pareto_fronts = "auto",
  plot_folder   = plot_dir,
  csv_out       = "all"
)

pareto_df <- OutputCollect$allPareto
best_model <- pareto_df$solID[which.min(pareto_df$decomp.rssd)]

tryCatch({
  robyn_onepagers(
    InputCollect  = InputCollect,
    OutputCollect = OutputCollect,
    select_model  = best_model,
    plot_folder   = plot_dir
  )
}, error = function(e) cat("One-pager warning:", e$message, "
"))

AllocatorCollect <- tryCatch(
  robyn_allocator(
    InputCollect       = InputCollect,
    OutputCollect      = OutputCollect,
    select_model       = best_model,
    scenario           = "max_response",
    total_budget       = 1000000,
    channel_constr_low = 0.1,
    channel_constr_up  = 0.9,
    plot_folder        = plot_dir
  ),
  error = function(e) { cat("Allocator warning:", e$message, "
"); NULL }
)

alloc_csv_path <- "outputs/models/robyn_allocation.csv"
if (!is.null(AllocatorCollect)) {
  tryCatch({
    alloc_dt <- AllocatorCollect$dt_optimOut
    fwrite(alloc_dt, alloc_csv_path)
  }, error = function(e) cat("Alloc table warning:", e$message, "
"))
}

roas_dt <- OutputCollect$xDecompAgg[solID == best_model]
fwrite(roas_dt, "outputs/models/robyn_roas.csv")

robyn_subfolders <- list.dirs(plot_dir, recursive = FALSE)
actual_plot_dir  <- if (length(robyn_subfolders) > 0)
                       tail(sort(robyn_subfolders), 1) else plot_dir

meta <- list(
  selected_model  = best_model,
  n_pareto_models = nrow(pareto_df),
  plot_dir        = actual_plot_dir,
  nrmse           = round(pareto_df$nrmse[pareto_df$solID == best_model], 4),
  rssd            = round(pareto_df$decomp.rssd[pareto_df$solID == best_model], 4),
  rsq_train       = round(pareto_df$rsq_train[pareto_df$solID == best_model], 4),
  robyn_version   = as.character(packageVersion("Robyn")),
  iterations      = 200,
  trials          = 1
)
write_json(meta, "outputs/models/robyn_meta.json", auto_unbox = TRUE)
cat("Selected model:", best_model, "
")
cat("Metadata saved to outputs/models/robyn_meta.json
")
