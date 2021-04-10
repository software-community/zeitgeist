from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewsSitemap(Sitemap):
    changefreq = "hourly"
    protocol = "https"
    priorities = {
        "main_page_home": 0.9,
        "tech_events": 0.8,
        "cult_events": 0.8,
        "merchandise": 0.8,
        "workshop": 0.7,
        "TSP:home": 0.6,
        "campus_ambassador_home": 0.6,
    }

    def items(self):
        return list(self.priorities.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priorities[item]
