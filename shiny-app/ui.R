library(datasets)

fluidPage(    
  
  titlePanel("Najlepsze ogloszenia OLX"),
  
  sidebarLayout(      
    
    sidebarPanel(
      selectInput("max", "Liczba najlepszych:", 
                  choices=c("3","5","10", "15", "20", "25", "30")),
      hr()
    ),
    
    mainPanel(
      plotOutput("OLXPlot")  
    )
  )
)