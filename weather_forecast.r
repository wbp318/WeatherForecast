# Install and load required packages
if (!require(pacman)) install.packages("pacman")
pacman::p_load(httr, jsonlite, ggplot2, gridExtra, lubridate)

# OpenWeather API key, city, and state
API_KEY <- "58cef9659cdf58d5e41f169d59e058dd"
CITY <- "New York"
STATE <- "NY"

# Function to get weather data
get_weather_data <- function(city, state, api_key) {
  base_url <- "http://api.openweathermap.org/data/2.5/forecast"
  response <- GET(url = base_url,
                  query = list(q = paste(city, state, "US", sep = ","),
                               appid = api_key,
                               units = "metric"))
  
  content <- content(response, "text")
  weather_data <- fromJSON(content)
  return(weather_data)
}

# Get weather data
weather_data <- get_weather_data(CITY, STATE, API_KEY)

# Process data
forecast <- weather_data$list[seq(1, 40, by = 8), ]  # Every 24 hours
forecast$dt <- as.POSIXct(forecast$dt, origin = "1970-01-01")
forecast$date <- format(forecast$dt, "%Y-%m-%d")
forecast$temp <- forecast$main$temp
forecast$description <- sapply(forecast$weather, function(x) x$description[1])

# Create temperature plot
temp_plot <- ggplot(forecast, aes(x = date, y = temp, group = 1)) +
  geom_line(color = "red", size = 1.2) +
  geom_point(color = "red", size = 3) +
  theme_minimal() +
  labs(title = "5-Day Temperature Forecast",
       x = "Date", y = "Temperature (°C)") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Create weather description plot
desc_plot <- ggplot(forecast, aes(x = date, y = 1, fill = description)) +
  geom_tile() +
  scale_fill_brewer(palette = "Set3") +
  theme_minimal() +
  labs(title = "Weather Description",
       x = "Date", y = NULL, fill = "Description") +
  theme(axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))

# Combine plots
infographic <- grid.arrange(
  temp_plot, desc_plot,
  ncol = 1,
  top = textGrob(paste("Weather Forecast for", CITY, STATE),
                 gp = gpar(fontsize = 16, fontface = "bold"))
)

# Save the infographic
ggsave("weather_infographic.png", infographic, width = 10, height = 8, dpi = 300)

print("Weather infographic has been generated and saved as 'weather_infographic.png'.")