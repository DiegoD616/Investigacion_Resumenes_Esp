NOMBRE_ARCHIVO_espanol = "./datos_salida/Resumenes_generados_espanol.csv"
NOMBRE_ARCHIVO_ingles  = "./datos_salida/Resumenes_generados_ingles.csv"

datos = read.csv(NOMBRE_ARCHIVO_espanol)

datos$TextRankSummarizer.rouge2.precision <- as.numeric(sub(",",".",datos$TextRankSummarizer.rouge2.precision))
datos$TextRankSummarizer.rouge2.exhautividad <- as.numeric(sub(",",".",datos$TextRankSummarizer.rouge2.exhautividad))
datos$TextRankSummarizer.rougeL.precision <- as.numeric(sub(",",".",datos$TextRankSummarizer.rougeL.precision))
datos$TextRankSummarizer.rougeL.exhautividad <- as.numeric(sub(",",".",datos$TextRankSummarizer.rougeL.exhautividad))

datos$LsaSummarizer.rouge2.precision <- as.numeric(sub(",",".",datos$LsaSummarizer.rouge2.precision))
datos$LsaSummarizer.rouge2.exhautividad <- as.numeric(sub(",",".",datos$LsaSummarizer.rouge2.exhautividad))
datos$LsaSummarizer.rougeL.precision <- as.numeric(sub(",",".",datos$LsaSummarizer.rougeL.precision))
datos$LsaSummarizer.rougeL.exhautividad <- as.numeric(sub(",",".",datos$LsaSummarizer.rougeL.exhautividad))


mean(datos$TextRankSummarizer.rouge2.precision)
mean(datos$TextRankSummarizer.rouge2.exhautividad)
mean(datos$TextRankSummarizer.rougeL.precision)
mean(datos$TextRankSummarizer.rougeL.exhautividad)

mean(datos$LsaSummarizer.rouge2.precision)
mean(datos$LsaSummarizer.rouge2.exhautividad)
mean(datos$LsaSummarizer.rougeL.precision)
mean(datos$LsaSummarizer.rougeL.exhautividad)
