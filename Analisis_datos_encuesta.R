library("irr")
library("dplyr")
library("data.table")

DIR_DATOS_ENCUESTA_TEXT_RANK = "./datos_encuesta/Resultados_encuentas-TextRank.csv"
DIR_DATOS_ENCUESTA_LSA       = "./datos_encuesta/Resultados_encuesta-LSA.csv"

Resultados_encuentas.TextRank <- read.csv(DIR_DATOS_ENCUESTA_TEXT_RANK)
Resultados_encuentas.LSA      <- read.csv(DIR_DATOS_ENCUESTA_LSA)

Resultados_encuentas.TextRank = Resultados_encuentas.TextRank %>% 
  select(-Marca.temporal) %>%
  rename(Coherencia    = El.resumen.presenta.frases.coherentes.) %>%
  rename(Concentracion = Casi.todos.los.puntos.importantes.de.la.noticia.están.representados.) %>%
  rename(Redundancia   = Algunas.frases.del.resumen.transmiten.el.mismo.significado.)

Resultados_encuentas.LSA = Resultados_encuentas.LSA %>% 
  select(-Marca.temporal) %>%
  rename(Coherencia    = El.resumen.presenta.frases.coherentes) %>%
  rename(Concentracion = Casi.todos.los.puntos.importantes.de.la.noticia.están.representados.) %>%
  rename(Redundancia   = Algunas.frases.del.resumen.transmiten.el.mismo.significado.)

kappam.fleiss(as.data.frame(t(Resultados_encuentas.TextRank)), detail = TRUE)
kappam.fleiss(as.data.frame(t(Resultados_encuentas.LSA))     , detail = TRUE)