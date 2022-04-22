# Water Poverty in Tanzania

## Author:
---

- Saad Saeed: 
[LinkedIn](https://www.linkedin.com/in/saadsaeed85/) |
[GitHub](https://github.com/ssaeed85) |
[Email](mailto:saadsaeed85@gmail.com)

# Business Problem:
---
>According to WHO, one out of six people lack access to safe drinking water in Tanzania (WHO/UNICEF, 2004).\
-https://projectzawadi.org/water-shortage/

> It is estimated that Tanzania spends 70 per cent of its health budget on preventable WASH _(Water, Sanitation and Hygiene)_ -related diseases as the majority of the population does not have access to improved sanitation, and close to half of the population does not have access to clean drinking water.\
-https://www.unicef.org/tanzania/what-we-do/wash

Resolving the water poverty crisis has been an ongoing agenda for the Tanzanian government water body for decades now. The Tanzanian government in conjunction with various charity efforts and the villages themselves has made major strides in improving the life of the Tanzanian people.

>In the year 2000, 73 percent of Tanzanians were living without basic access to safe water. The most up-to-date numbers from 2017 show that the percentage was nearly halved and continues to fall.\
-https://lifewater.org/blog/tanzania-water-crisis-facts/

Looking at past water well data, I believe we can help the Tanzanian government get closer to its 2025 vision of improved sanitation to 95 per cent of its people. I believe a predictive model that helps identify water wells in a state of disrepair can help the Tanzanian water body better allocate its resources.

# Data:
---
The data was gathered from [drivendata.com](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/). The dataset covers nearly 55,000 different water well sites across the years going as far back as 1960. 

The primary hurdle in this dataset has been to account for incomplete data or missing data.

# Hurdles:
---
Nearly 35% of the water wells have a construction year of 0.

1800 water well sites share the same GPS coordinates and have a recorded location off the west coast of Africa.

![img](./images/BadCoordinates.png)

All of these sites are associated with wellwater projects in the northern Tanzania in the regions of Mwanza and Shinyanga. We resolved this by using median coordinate values in each of these regions.

![img](./images/MwanzaAndShinyanga.png)

We understand that data gathering and standardization of data being gathered is ongoing effort. We just want to emphasize the value of good data. With better and more accurate data, our model predictions should improve significantly.


# Methodology:
---

A variety of different data science techniques were used to improve estimation including. Through an iterative process we were able to generate a final classification report.

![img](./images/ClassificationReport.png)

Our overall classification accuracy is about 80%. One area we really need to improve on is our ability to predict water well sites that are in need of repair.

# Further steps:
---
- Given more time we'd like to look into how the remoteness/accessibility of how a water well site compared to its region of origin has an effect on our predictive capabilities
- Try to improve our predictions on water wells that need repairs so we can address issues before failure
- Implement a time series model to help predict when a water well might fail
- Oversampling our underrepresented data.
