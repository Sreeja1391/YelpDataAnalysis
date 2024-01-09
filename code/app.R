#app.R
#App1
#Menu options
library(shiny)
library(leaflet)
library(dplyr)
library(shinythemes)
library(tidyverse)

df <- read_csv("Philadelphia_Veg_data.csv")

filtered_file <- read_csv("filtered_file.csv")

filtered_file$filtered_item <- lapply(
  filtered_file$filtered_item,
  function(x) {
    gsub("'", "", strsplit(gsub("\\[|\\]", "", x), ",")[[1]])
  }
)

aggregated_data <- read_csv("aggregated_rest&item_rcmd.csv")

aggregated_data$item <- lapply(
  aggregated_data$item,
  function(x) {
    gsub("'", "", strsplit(gsub("\\[|\\]", "", x), ",")[[1]])
  }
)

ui <- fluidPage(
  titlePanel("GreenEats: Navigating Top Vegan & Veggie Cuisine"),
  theme = shinytheme("flatly"),
  wellPanel(
    p("Welcome to our Yelp Review Analysis app!",
      br(),
      "We've got your back if you're a vegetarian or vegan in Philadelphia. Use our map to explore the top-rated plant-based restaurants in your area.",
      br(),
      "Pick a postal code, click a marker, and discover restaurant details and popular dishes.")
  ),
  fluidRow(
    column(
      width = 2,
      selectizeInput(
        "postalCode", "Select Postal Code",
        choices = c("All", unique(filtered_file$postal_code)),
        selected = "All",
        options = list(
          placeholder = "Select a Postal Code",
          onInitialize = I('function() { this.setValue(""); }')
        )
      ),
      uiOutput("menuOptions")
    ),
    column(
      width = 10,
      fluidRow(
        column(
          width = 12,
          leafletOutput("map")
        ),
        column(
          width = 12,
          htmlOutput("selectedItems")
        )
      )
    )
  )
)

server <- function(input, output, session) {
  
  filteredData <- reactive({
    if (input$postalCode == "All") {
      df
    } else {
      subset(df, postal_code == as.numeric(input$postalCode))
    }
  })
  
  output$map <- renderLeaflet({
    leaflet() |>
      addTiles() |>
      addMarkers(
        data = filteredData(),
        clusterOptions = markerClusterOptions(),
        popup = ~paste("Restaurant Name: ", filteredData()$name)
      ) |>
      setView(
        lng = mean(filteredData()$longitude),
        lat = mean(filteredData()$latitude),
        zoom = 13
      )
  })
  
  output$selectedItems <- renderPrint({
    click_info <- input$map_marker_click
    
    if (is.null(click_info) && input$postalCode != "All") {
      cat("<div style='color: red; font-size: 16px;'>No business selected.</div>")
    } else if (!is.null(click_info)) {
      click_lat <- click_info$lat
      click_lng <- click_info$lng
      
      selected_business <- filteredData() %>%
        filter(latitude == click_lat, longitude == click_lng) %>%
        pull(name)
    
      if(is_empty(selected_business)){
        cat("<div style='color: red; font-size: 16px;'>No business selected.</div>")
      }
      else if (!is.null(selected_business)) {
        selected_restaurant <- aggregated_data %>%
          filter(name %in% selected_business)
        
        if (nrow(selected_restaurant) > 0) {
          cat("<div style='color: #333; font-size: 18px; font-weight: bold;'>Details for the selected business:</div>")
          cat("<div><b>Restaurant Name:</b>", selected_restaurant$name, "</div>")
          cat("<div><b>Rating on Yelp:</b>", selected_restaurant$rest_stars, "</div>")
          cat("<div><b>Number of Reviews:</b>", selected_restaurant$review_count, "</div>")
          selected_items <- aggregated_data$item[aggregated_data$name %in% selected_business]
          
          if (length(selected_items) > 0) {
            cat("<div style='color: green; font-size: 16px; margin-top: 10px;'>Popular Items from reviews:</div>")
            cat("<ul>")
            cat(paste("<li> ", trimws(selected_items[[1]]), "</li>", collapse = "\n"))
            cat("</ul>")
          } else {
            cat("<div style='color: orange; font-size: 16px; margin-top: 10px;'>No items found for the selected business.</div>")
          }
          
        } else {
          cat("<div style='color: red; font-size: 16px;'>No information found for the selected business.</div>")
        }
      }
    } else if (is.null(click_info) && input$postalCode == "All") {
      cat("<div style='color: red; font-size: 16px;'>No business selected.</div>")
    }
  })
  
  
  output$menuOptions <- renderUI({
    if (!is.null(filteredData())) {
      postal_code_selected <- as.numeric(input$postalCode)
      popular_items <- filtered_file$filtered_item[
        filtered_file$postal_code == postal_code_selected
      ]
      
      if (length(popular_items) > 0) {
        shuffled_items <- sample(popular_items[[1]])
        tagList(
          div(
            p("Popular items in the selected area from the reviews:", style = "font-weight: bold;"),
            tags$ul(
              lapply(shuffled_items, function(item) {
                tags$li(
                  tags$i(class = "fas fa-check-circle", style = "color: #4CAF50; margin-right: 5px;"),
                  item
                )
              })
            ),
            style = "background-color: #E5E4E2; padding: 10px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);"
          )
        )
      } else {
        p("No popular items found for the selected area.")
      }
    }
  })
  
}

shinyApp(ui, server)