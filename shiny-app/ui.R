library(datasets)

fluidPage(    
  
  titlePanel("Najlepsze ogloszenia OLX"),
  fluidRow(      
    mainPanel(
      selectInput("max", "Liczba najlepszych:", 
                  choices=c("3","5","10", "15", "20", "25", "30"),
                  selected=10),
       hr(),
      plotOutput("OLXPlot")  
    )
  )
)
