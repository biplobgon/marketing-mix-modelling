# =============================================================================
# R Package Installation Script for Marketing Mix Modelling Project
# Run once: Rscript install_r_packages.R
# =============================================================================

options(repos = c(CRAN = "https://cloud.r-project.org"))

# Use user-writable library (avoids needing admin access to Program Files)
R_LIBS_USER <- "C:/Rlibs"
dir.create(R_LIBS_USER, showWarnings = FALSE, recursive = TRUE)
.libPaths(c(R_LIBS_USER, .libPaths()))
cat(sprintf("Using library: %s\n", R_LIBS_USER))

cat("Installing core packages...\n")
core_pkgs <- c("dplyr", "tidyr", "ggplot2", "data.table", "lubridate",
               "scales", "jsonlite", "readr", "stringr", "purrr")
install.packages(core_pkgs, lib = R_LIBS_USER, quiet = TRUE)

cat("Installing reticulate (R-Python bridge)...\n")
install.packages("reticulate", lib = R_LIBS_USER, quiet = TRUE)

cat("Installing IRkernel (Jupyter R kernel)...\n")
install.packages("IRkernel", lib = R_LIBS_USER, quiet = TRUE)

cat("Installing Robyn dependencies...\n")
robyn_deps <- c("doParallel", "foreach", "glmnet", "minpack.lm",
                "rPref", "StanHeaders", "prophet")
install.packages(robyn_deps, lib = R_LIBS_USER, quiet = TRUE)

cat("Installing Robyn...\n")
install.packages("Robyn", lib = R_LIBS_USER, quiet = TRUE)

cat("\n=== Verifying installations ===\n")
pkgs <- c("Robyn", "reticulate", "IRkernel", "dplyr", "data.table",
          "ggplot2", "prophet", "glmnet")
for (p in pkgs) {
  if (requireNamespace(p, quietly = TRUE)) {
    v <- as.character(packageVersion(p))
    cat(sprintf("  [OK] %-15s %s\n", p, v))
  } else {
    cat(sprintf("  [FAILED] %s\n", p))
  }
}
cat("\nDone.\n")
