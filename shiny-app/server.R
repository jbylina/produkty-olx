library(datasets)
url<-"https://projects.rapit.pw/produkty-olx/Top_10.csv"
top30 <- read.csv(url, header=FALSE, sep=",")
names(top30) <- c("V1","V2","V3")
# Define a server for the Shiny app
function(input, output) {
  
  output$OLXPlot <- renderPlot({
    
    barplot(top30$V3[1:input$max], top30$V1[1:input$max], 
            names.arg=top30$V1[1:input$max],
            las=2,
            ylab="Liczba wyswietlen",
            xlab="")
  })
}
