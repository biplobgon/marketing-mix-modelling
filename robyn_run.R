# =============================================================================
# Robyn MMM - Indian FMCG National Weekly
# =============================================================================

lib_path <- "C:/Rlibs"
if (!dir.exists(lib_path)) dir.create(lib_path, recursive = TRUE, showWarnings = FALSE)
tmp_dir <- "C:/Rtemp"
if (!dir.exists(tmp_dir)) dir.create(tmp_dir, recursive = TRUE, showWarnings = FALSE)
Sys.setenv(TMP = tmp_dir, TEMP = tmp_dir)

.libPaths(c(lib_path, .libPaths()))
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
cat("Rows:", nrow(dt), "| Cols:", ncol(dt), "\n")
cat("Date range:", format(min(dt$date)), "to", format(max(dt$date)), "\n")

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

cat("\n=== Running Nevergrad (iterations=200, trials=1, cores=2) ===\n")
OutputModels <- robyn_run(
  InputCollect = InputCollect,
  cores        = 2,
  iterations   = 200,
  trials       = 1,
  outputs      = FALSE
)
cat("=== Optimisation complete ===\n")

plot_dir <- "outputs/figures/robyn"
dir.create(plot_dir, showWarnings = FALSE, recursive = TRUE)

OutputCollect <- robyn_outputs(
  InputCollect  = InputCollect,
  OutputModels  = OutputModels,
  pareto_fronts = "auto",
  plot_folder   = plot_dir,
  csv_out       = "all"
)

extract_pareto_df <- function(output_collect) {
  candidates <- list(
    output_collect$allPareto,
    output_collect$resultHypParam,
    output_collect$allPareto$resultHypParam
  )
  for (cand in candidates) {
    if (is.data.frame(cand)) return(as.data.frame(cand))
  }
  stop("Unable to locate Pareto table. OutputCollect names: ",
       paste(names(output_collect), collapse = ", "),
       " | allPareto names: ",
       paste(names(output_collect$allPareto), collapse = ", "))
}

pareto_df <- extract_pareto_df(OutputCollect)

model_id_col <- if ("solID" %in% names(pareto_df)) {
  "solID"
} else if ("sol_id" %in% names(pareto_df)) {
  "sol_id"
} else if ("sol.id" %in% names(pareto_df)) {
  "sol.id"
} else {
  NA_character_
}

best_model <- NA_character_
if ("selectID" %in% names(OutputCollect) && length(OutputCollect$selectID) > 0) {
  best_model <- as.character(OutputCollect$selectID[[1]])
}

if (is.na(best_model) || !nzchar(best_model)) {
  if (is.na(model_id_col)) {
    stop("No model ID column found in Pareto table. Available columns: ",
         paste(names(pareto_df), collapse = ", "))
  }
  best_model <- as.character(pareto_df[[model_id_col]][which.min(pareto_df$decomp.rssd)][1])
}

if (is.na(best_model) || !nzchar(best_model)) {
  if (is.na(model_id_col)) {
    stop("Unable to resolve selected model ID.")
  }
  best_model <- as.character(pareto_df[[model_id_col]][1])
  cat("Fallback: using first Pareto model as selected model ->", best_model, "\n")
}

if (FALSE) {
  tryCatch({
    robyn_onepagers(
      InputCollect  = InputCollect,
      OutputCollect = OutputCollect,
      select_model  = best_model,
      plot_folder   = plot_dir
    )
  }, error = function(e) cat("One-pager warning:", e$message, "\n"))
} else {
  cat("Skipping robyn_onepagers() for notebook stability on Windows.\n")
}

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
  error = function(e) { cat("Allocator warning:", e$message, "\n"); NULL }
)

alloc_csv_path <- "outputs/models/robyn_allocation.csv"
if (!is.null(AllocatorCollect)) {
  tryCatch({
    alloc_dt <- AllocatorCollect$dt_optimOut
    fwrite(alloc_dt, alloc_csv_path)
  }, error = function(e) cat("Alloc table warning:", e$message, "\n"))
}

xdecomp <- OutputCollect$xDecompAgg
if (!is.na(model_id_col) && model_id_col %in% names(xdecomp)) {
  roas_dt <- xdecomp[xdecomp[[model_id_col]] == best_model, , drop = FALSE]
} else {
  cat("xDecompAgg has no matching model ID column; exporting full decomposition table.\n")
  roas_dt <- xdecomp
}
fwrite(roas_dt, "outputs/models/robyn_roas.csv")

robyn_subfolders <- list.dirs(plot_dir, recursive = FALSE)
actual_plot_dir  <- if (length(robyn_subfolders) > 0)
                       tail(sort(robyn_subfolders), 1) else plot_dir

meta <- list(
  selected_model  = best_model,
  n_pareto_models = nrow(pareto_df),
  plot_dir        = actual_plot_dir,
  nrmse           = if ("nrmse" %in% names(pareto_df)) round(pareto_df$nrmse[1], 4) else NA_real_,
  rssd            = if ("decomp.rssd" %in% names(pareto_df)) round(pareto_df$decomp.rssd[1], 4) else NA_real_,
  rsq_train       = if ("rsq_train" %in% names(pareto_df)) round(pareto_df$rsq_train[1], 4) else NA_real_,
  robyn_version   = as.character(packageVersion("Robyn")),
  iterations      = 200,
  trials          = 1
 )

if (!is.na(model_id_col) && model_id_col %in% names(pareto_df)) {
  sel_rows <- pareto_df[as.character(pareto_df[[model_id_col]]) == best_model, , drop = FALSE]
  if (nrow(sel_rows) > 0) {
    if ("nrmse" %in% names(sel_rows)) meta$nrmse <- round(sel_rows$nrmse[1], 4)
    if ("decomp.rssd" %in% names(sel_rows)) meta$rssd <- round(sel_rows$decomp.rssd[1], 4)
    if ("rsq_train" %in% names(sel_rows)) meta$rsq_train <- round(sel_rows$rsq_train[1], 4)
  }
}

write_json(meta, "outputs/models/robyn_meta.json", auto_unbox = TRUE)
cat("Selected model:", best_model, "\n")
cat("Metadata saved to outputs/models/robyn_meta.json\n")
