setwd("/Users/lucas/OneDrive/Documentos/metaOtimizador/pythonToR")
library(reticulate)
library(cmaes)
#library(stats)
#library(doParallel)
library(irace)
library(GA)

pymoo <- import("pymoo")
GA <- pymoo$algorithms$soo$nonconvex$ga$GA
get_problem <- pymoo$problems$get_problem
minimize <- pymoo$optimize

source_python("ga_test.py")
teste()

#configuracao para a sintonia de parametros
parametros.tabela <- '
pop_size "" i (50, 100)
eliminate_duplicates "" i (0, 1)
'

#le tabela para o irace
parameters <- readParameters(text = parametros.tabela)

#funcao para avaliar cada candidato de configuracao em uma instancia
target.runner <- function(experiment, scenario) {
  instances <- experiment$instance
  configuration <- experiment$configuration

  #executa o GA
  GA <- ga(pop_size = as.numeric(configuration[['pop_size']]), eliminate_duplicates = as.numeric(configuration[['eliminate_duplicates']]))
  
  #print(GA@fitnessValue)
  return (list(cost = GA@res.F))
}
