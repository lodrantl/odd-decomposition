library(tidyverse)
Sys.setlocale(category = "LC_ALL", locale = "Slovenian")

small_graphs_isom <- read_csv(
  "small_graphs.csv",
  col_types = cols(
    .default = col_integer(),
    percentage = col_double(),
    time = col_double()
  )
)
small_graphs <- read_csv(
  "small_graphs_isomorphic.csv",
  col_types = cols(
    .default = col_integer(),
    percentage = col_double(),
    time = col_double()
  )
)
graphs <- rbind(small_graphs, small_graphs_isom)
graphs$vrsta <- 1
graphs$vrsta[1:nrow(small_graphs)] <- 0
graphs$vrsta <- factor(graphs$vrsta)

p1 <- ggplot(graphs, aes(x=n, color = vrsta)) +
  geom_line(size=1.5, aes(y = percentage / 100)) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  scale_color_hue(labels = c("izomorfni", "vsi")) +
  labs(title="Uspešnost razbitja na dva liha podgrafa", x="Število oglišč", y="Uspešnost")
print(p1)

p2 <- ggplot(small_graphs_isom, aes(x=n)) +
  geom_line(aes(y = all, colour="vsi primeri")) +
  geom_line(aes(y = decomposable, colour="uspešni primeri razbiti")) +
  geom_line(aes(y = time*8000, colour="čas izvajanja")) +
  scale_y_continuous("Število primerov", sec.axis = sec_axis(~ . / 8000, name = "Čas [s]")) +
  labs(title="Število primerov", x="Število oglišč") +
  theme(legend.title = element_blank())
#print(p2)





