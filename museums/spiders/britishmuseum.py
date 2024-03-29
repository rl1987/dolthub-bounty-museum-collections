import scrapy
from scrapy.selector import Selector

import json
from urllib.parse import urlparse, parse_qsl, urlencode, urljoin

from museums.items import ObjectItem


class BritishmuseumSpider(scrapy.Spider):
    name = "britishmuseum"
    allowed_domains = ["britishmuseum.org"]
    start_urls = [
        "https://www.britishmuseum.org/api/_search?&view=grid&sort=object_name__asc&page=0"
    ]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0], method="POST", callback=self.parse_search_api_response
        )

    def parse_search_api_response(self, response):
        json_dict = json.loads(response.text)

        if json_dict.get("error") is not None:
            yield scrapy.Request(
                response.url,
                callback=self.parse_search_api_response,
                meta={"dont_cache": True},
                dont_filter=True,
            )

        hits = json_dict.get("hits", dict()).get("hits", [])

        if len(hits) == 0:
            return

        for hit in hits:
            api_id = hit.get("_id")

            source_dict = hit.get("_source", dict())

            unique_object_id = None
            for id_dict in source_dict.get("identifier", []):
                if id_dict.get("type") == "unique object id":
                    unique_object_id = id_dict.get("unique_object_id")
                    break

            if unique_object_id is not None:
                url = "https://www.britishmuseum.org/api/_object?id=" + unique_object_id
                yield scrapy.Request(url, callback=self.parse_object_api_response)

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        new_params = dict(old_params)
        new_params["page"] = int(new_params["page"]) + 1

        next_page_url = "https://www.britishmuseum.org/api/_search?&" + urlencode(
            new_params
        )

        yield scrapy.Request(
            next_page_url, method="POST", callback=self.parse_search_api_response
        )

    def parse_object_api_response(self, response):
        json_dict = json.loads(response.text)
        source_dict = json_dict.get("hits", dict()).get("hits")[0].get("_source")

        o = urlparse(response.url)

        params = dict(parse_qsl(o.query))

        item = ObjectItem()

        item["object_number"] = params.get("id")

        item["institution_name"] = "British Museum"
        item["institution_city"] = "London"
        item["institution_country"] = "United Kingdom"
        item["institution_latitude"] = 51.518757
        item["institution_longitude"] = -0.126168

        # XXX: category

        xtemplate_full_json_str = source_dict.get("xtemplate", dict()).get("full")
        xtemplate_full_json_dict = json.loads(xtemplate_full_json_str)

        if type(xtemplate_full_json_dict.get("Title")) == list:
            title_parts = []

            for title_html in xtemplate_full_json_dict.get("Title", []):
                sel = Selector(text=title_html)
                title_part = " ".join(sel.xpath("//text()").getall())
                title_parts.append(title_part)

            item["title"] = " ".join(title_parts)
        elif type(xtemplate_full_json_dict.get("Title")) == str:
            title_html = xtemplate_full_json_dict.get("Title")
            sel = Selector(text=title_html)
            item["title"] = " ".join(sel.xpath("//text()").getall())

        item["department"] = xtemplate_full_json_dict.get("Department")
        item["description"] = " ".join(xtemplate_full_json_dict.get("Description", []))

        description_parts = []

        for d in xtemplate_full_json_dict.get("Description", []):
            sel = Selector(text=d)
            description_parts.append(" ".join(sel.xpath("//text()").getall()))

        item["description"] = " ".join(description_parts)

        item["current_location"] = xtemplate_full_json_dict.get("Location")
        if item.get("current_location") is not None and "<span" in item.get(
            "current_location"
        ):
            sel = Selector(text=item.get("current_location"))
            item["current_location"] = "".join(sel.xpath("//text()").getall())

        dimensions = []

        for dimension_html in xtemplate_full_json_dict.get("Dimensions", []):
            sel = Selector(text=dimension_html)
            dimension = " ".join(sel.xpath("//text()").getall())
            dimensions.append(dimension)

        item["dimensions"] = "|".join(dimensions)

        if type(xtemplate_full_json_dict.get("$Inscriptions")) == list:
            inscriptions = []

            for inscription_dict in xtemplate_full_json_dict.get("$Inscriptions"):
                content = inscription_dict.get("Inscription content")
                if content is not None:
                    inscriptions.append(content)

            item["inscription"] = "|".join(inscriptions)

        if type(xtemplate_full_json_dict.get("Materials")) == dict:
            materials_html = xtemplate_full_json_dict.get("Materials").get("value")
            sel = Selector(text=materials_html)
            item["materials"] = " ".join(sel.xpath("//text()").getall())
        elif type(xtemplate_full_json_dict.get("Materials")) == list:
            materials = []

            for material_dict in xtemplate_full_json_dict.get("Materials"):
                materials_html = material_dict.get("value")
                sel = Selector(text=materials_html)
                materials.append(sel.xpath('//span[@class="vterm"]/text()').get())

            item["materials"] = "|".join(materials)

        if type(xtemplate_full_json_dict.get("Technique")) == dict:
            technique_html = xtemplate_full_json_dict.get("Technique").get("value")
            sel = Selector(text=technique_html)
            item["technique"] = " ".join(sel.xpath("//text()").getall())

        if type(xtemplate_full_json_dict.get("Findspot")) == list:
            findspots = []

            for findspot_dict in xtemplate_full_json_dict.get("Findspot"):
                value_html = findspot_dict.get("value")
                sel = Selector(text=value_html)
                findspots.append(sel.xpath('//span[@class="vterm"]/text()').get())

            item["from_location"] = "|".join(findspots)

        if type(xtemplate_full_json_dict.get("Cultures/periods")) == dict:
            culture_html = xtemplate_full_json_dict.get("Cultures/periods").get("value")
            sel = Selector(text=culture_html)
            item["culture"] = sel.xpath('//span[@class="vterm"]/text()').get()

        if type(xtemplate_full_json_dict.get("Producer name")) == dict:
            author_html = xtemplate_full_json_dict.get("Producer name").get("value")
            sel = Selector(text=author_html)
            item["maker_full_name"] = sel.xpath('//span[@class="vterm"]/text()').get()

        item["acquired_year"] = xtemplate_full_json_dict.get("Acquisition date")
        if item.get("acquired_year") is not None and "<span" in item.get(
            "acquired_year"
        ):
            html_str = item["acquired_year"]
            sel = Selector(text=html_str)
            item["acquired_year"] = sel.xpath("//text()").get()

        if type(xtemplate_full_json_dict.get("Acquisition name")) == dict:
            name_html = xtemplate_full_json_dict.get("Acquisition name").get("value")
            sel = Selector(text=name_html)
            item["acquired_from"] = sel.xpath('//span[@class="vterm"]/text()').get()

        item["date_description"] = xtemplate_full_json_dict.get("Production date")
        if item.get("date_description") is not None and "<span" in item.get(
            "date_description"
        ):
            dd = item["date_description"]
            sel = Selector(text=dd)
            item["date_description"] = " ".join(sel.xpath("//text()").getall())

        credit_line = None
        image_url = None

        for mm_dict in source_dict.get("multimedia", []):
            credit_line = mm_dict.get("legal", dict()).get("credit_line")

            if mm_dict.get("type", dict()).get("type") == "image":
                image_url = (
                    mm_dict.get("processed", dict())
                    .get("preview", dict())
                    .get("location")
                )
            if credit_line is not None and image_url is not None:
                break

        if image_url is not None:
            image_url = urljoin("http://media.britishmuseum.org/media/", image_url)

        item["credit_line"] = credit_line
        item["image_url"] = image_url

        item[
            "source_1"
        ] = "https://www.britishmuseum.org/collection/object/" + params.get("id")
        item["source_2"] = response.url

        yield item


# UPDATE `objects` SET `date_description` = REPLACE(`date_description`, '</span>', '') WHERE `date_description` LIKE "%</span>%";
# UPDATE `objects` SET `date_description` = REPLACE(`date_description`, '<span class="vsuffix">', '') WHERE `date_description` LIKE "%<span%";
