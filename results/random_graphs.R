library(tidyverse)
Sys.setlocale(category = "LC_ALL", locale = "Slovenian")

graphs <- read_csv(
  "random_graphs.csv",
  col_types = cols(
    .default = col_integer(),
    percentage = col_double(),
    time = col_double()
  )
)

graphs$n <- factor(graphs$n)

p1 <- ggplot(graphs, aes(x=m, color = n)) +
  geom_line(size=1.5, aes(y = percentage / 500)) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(title="Vpliv števila povezav", x="Število povezav", y="Uspešnost")
print(p1)





