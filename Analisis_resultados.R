library("dplyr")

NOMBRE_ARCHIVO_espanol = "./datos_salida/Resumenes_generados_espanol.csv"
NOMBRE_ARCHIVO_ingles  = "./datos_salida/Resumenes_generados_ingles.csv"

datos_espanol <- read.csv(NOMBRE_ARCHIVO_espanol, row.names=1, dec=",") %>% 
  select(-Texto.original, -Resumen.humano)
datos_ingles  <- read.csv(NOMBRE_ARCHIVO_ingles,  row.names=1, dec=",") %>% 
  select(-Texto.original, -Resumen.humano)

Rendimiento_resumidores <- data.frame (
  rouge2.precision     = double(),
  rouge2.exhaustividad = double(),
  rougeL.precision     = double(),
  rougeL.exhaustividad = double(),
  Resumidor            = character(),
  Idioma               = character(),
  stringsAsFactors     = FALSE
)

i = 1
idiomas = c("Español","Ingles")

for( datos in list(datos_espanol, datos_ingles)) {
  TextRank_temp = datos             %>% 
    select(starts_with("TextRank")) %>% 
    select(-TextRankSummarizer)     %>%
    mutate(Resumidor = "TextRank")  %>%
    rename(rouge2.precision = TextRankSummarizer.rouge2.precision) %>%
    rename(rouge2.exhaustividad = TextRankSummarizer.rouge2.exhautividad) %>%
    rename(rougeL.precision = TextRankSummarizer.rougeL.precision) %>%
    rename(rougeL.exhaustividad = TextRankSummarizer.rougeL.exhautividad)
  
  Lsa_temp = datos             %>% 
    select(starts_with("Lsa")) %>% 
    select(-LsaSummarizer)     %>%
    mutate(Resumidor = "Lsa")  %>%
    rename(rouge2.precision = LsaSummarizer.rouge2.precision) %>%
    rename(rouge2.exhaustividad = LsaSummarizer.rouge2.exhautividad) %>%
    rename(rougeL.precision = LsaSummarizer.rougeL.precision) %>%
    rename(rougeL.exhaustividad = LsaSummarizer.rougeL.exhautividad)
  
  Rendimiento_temp = bind_rows(TextRank_temp, Lsa_temp) %>% 
    mutate(Idioma = idiomas[i])

  Rendimiento_resumidores = bind_rows(Rendimiento_resumidores, Rendimiento_temp)
  i = i + 1
}

summary(Rendimiento_resumidores %>% select_if(is.numeric))

res.man <- manova(
  cbind(rouge2.precision, rouge2.exhaustividad, 
        rougeL.precision, rougeL.exhaustividad) ~ Idioma * Resumidor, 
  data = Rendimiento_resumidores)
summary(res.man)

par(mfrow=c(2,2))
two.way <- aov(rouge2.precision ~ Idioma * Resumidor,     data = Rendimiento_resumidores)
summary(two.way)
plot(two.way)

two.way <- aov(rougeL.precision ~ Idioma * Resumidor,     data = Rendimiento_resumidores)
summary(two.way)
plot(two.way)

two.way <- aov(rouge2.exhaustividad ~ Idioma * Resumidor, data = Rendimiento_resumidores)
summary(two.way)


two.way <- aov(rouge2.exhaustividad ~ Idioma * Resumidor, data = Rendimiento_resumidores)
summary(two.way)
plot(two.way)
par(mfrow=c(1,1))
tukey.two.way<-TukeyHSD(two.way)
plot(tukey.two.way)


two.way <- aov(rougeL.exhaustividad ~ Idioma * Resumidor, data = Rendimiento_resumidores)
summary(two.way)


two.way <- aov(rougeL.exhaustividad ~ Idioma + Resumidor, data = Rendimiento_resumidores)
summary(two.way)
plot(two.way)
tukey.two.way<-TukeyHSD(two.way)
tukey.two.way
