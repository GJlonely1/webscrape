# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Allows you to convert data from one format to another. E.g. Change Currency from pounds to dollars.
# Allows you to change data type from string to integer, remove signs, validate data, etc.
# You can use a pipeline to store data into a database

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()
        
        # Category & Product Type --> Switch to Lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys: 
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Price -> Convert to float
        price_keys = ['price','price_exclude_tax', 'price_include_tax', 'tax']
        for price_key in price_keys: 
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = value
        
        #Availability -> Extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2: 
            adapter['availability'] = 0
        else: 
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])
        
        # Reviews ->  Convert String to Number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        #  Stars -> Convert text to number
        stars_string = adapter.get('stars')
        stars_string_array = stars_string.split(' ')
        stars_text_value = stars_string_array[1].lower()
        if stars_text_value == "zero": 
            adapter['stars'] = 0
        elif stars_text_value == "one": 
            adapter['stars'] = 1
        elif stars_text_value == "two": 
            adapter['stars'] = 2
        elif stars_text_value == "three": 
            adapter['stars'] = 3
        elif stars_text_value == "four": 
            adapter['stars'] = 4
        elif stars_text_value == "five": 
            adapter['stars'] = 5

        return item
