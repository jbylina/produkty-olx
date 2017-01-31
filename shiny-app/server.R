library(datasets)

url<-"https://projects.rapit.pw/produkty-olx/Top_10.csv"
top30 <- read.csv(url, header=FALSE, sep=",")
names(top30) <- c("V1","V2","V3")
top30["V4"] <- gsub("-", " ", sub(".CID.*","",substring(top30$V2, 27)))
colfunc <- colorRampPalette(c("green", "red"))

function(input, output) {
  output$OLXPlot <- renderPlot({
    par(mar=c(10,30,0,2))
    barplot(top30$V3[1:input$max], top30$V1[1:input$max], 
            names.arg=top30$V4[1:input$max],
            col=colfunc(input$max),
            horiz=TRUE,
            las=1,
            ylab="",
            xlab="Liczba wyswietlen"
             )
  }, height=800, width=900)
}
