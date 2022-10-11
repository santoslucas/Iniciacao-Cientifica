library(stats)
library(doParallel)
library(irace)
library(reticulate)

setwd('/home/andre/prj-r/irace-ex/')

pymoo <- import('pymoo')
single_obj <- pymoo$problems$single
source_python('ga.py')

#configuracao para a sintonia de parametros
parametros.tabela <- '
pop_size "" i (50, 100)
p_cross "" r (0.5, 1.0)
eta_cross "" r (1.0, 30.0)
p_mut "" r (0.01, 0.2)
eta_mut "" r (1.0, 40.0)
eliminate_duplicates "" i (0, 1)
'

obj_funs <- c(1L, 2L, 3L)

#le tabela para o irace
parameters <- readParameters(text = parametros.tabela)

#funcao para avaliar cada candidato de configuracao em uma instancia
target.runner <- function(experiment, scenario) {
  instance <- experiment$instance
  # print(instances)
  configuration <- experiment$configuration
  
  # #funcao objetivo
  # fn <- function(x) {
  #   # print(x)
  #   # print(instances$evaluate(x))
  #   n = 2
  #   f <- instance(n_var = n)
  #   return (instance$evaluate(x))
  # }
  
  #executa o ga
  max_eval = 1000
  obj <- ga(instance, max_eval, 
     as.integer(configuration[['pop_size']]), 
     as.double(configuration[['p_cross']]),
     as.double(configuration[['eta_cross']]),
     as.double(configuration[['p_mut']]),
     as.double(configuration[['eta_mut']]),
     as.logical(configuration[['eliminate_duplicates']])
     )
  
  print(obj)
  return (list(cost = obj))
}

#configuracao do cenario
scenario <- list(targetRunner = target.runner,
                 instances = obj_funs,
                 maxExperiments = 300,
                 logFile = 'irace-log.txt')

#verifica se o cenario e valido
checkIraceScenario(scenario = scenario, parameters = parameters)

#executa o irace
tuned.confs <- irace(scenario = scenario, parameters = parameters)

#apresentar os melhores conjuntos de parametros para as tres funcoes objetivo
configurations.print(tuned.confs)

#testa as configuracoes
test <- function(configuration)
{
  res <- lapply(matrix(rep(obj_funs,each=1), nrow=length(obj_funs)*5),
                function(x) target.runner(
                  experiment = list(instance = x, configuration = configuration),
                  scenario = scenario)
                )
  return (sapply(res, getElement, name = "cost"))
}

default <- test(data.frame(pop_size=100, p_cross=1.0, eta_cross=3.0, p_mut=0.01, eta_mut=10, eliminate_duplicates=TRUE))

tuned1 <- test (removeConfigurationsMetaData(tuned.confs[1,]))

tuned2 <- test (removeConfigurationsMetaData(tuned.confs[2,]))

boxplot(list(default=default, tuned1=tuned1, tuned2=tuned2))

