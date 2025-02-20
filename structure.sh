#!/bin/bash

# Create principal directories
mkdir -p data/{raw,processed,external}
mkdir -p notebooks
mkdir -p src/{models,utils}
mkdir -p results/{figures,forecasts}
mkdir -p tests

# Crear archivos iniciales
touch data/raw/.gitkeep data/processed/.gitkeep data/external/.gitkeep
touch notebooks/.gitkeep
touch src/models/.gitkeep src/utils/.gitkeep
touch results/figures/.gitkeep results/forecasts/.gitkeep
touch tests/.gitkeep
touch .gitignore
touch README.md
touch structure.txt

# Mensaje de finalización
echo "Estructura del proyecto creada con éxito."