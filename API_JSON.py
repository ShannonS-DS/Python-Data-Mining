
# coding: utf-8

# In[17]:

#import urllib2
import json
import pandas as pd




resp_text = urllib.request.urlopen('https://www.coursera.org/maestro/api/topic/list?full=1+or+https%3A%2F%2Fwww.coursera.org%2Fmaestro%2Fapi%2Ftopic%2Flist2').read().decode('UTF-8')
# Use loads to decode from text
courses_data  = json.loads(resp_text)
#courses_data = courses_data['elements']


# In[54]:

courses_df = pd.DataFrame()
courses_df['course_name'] = [*map(lambda x: x['name'], courses_data)]
courses_df['course_language'] = [*map(lambda course_data: course_data['language'], courses_data)]
courses_df['course_short_name'] = [*map(lambda course_data: course_data['short_name'], courses_data)]

courses_df['universities'] = [*map(lambda course_data: course_data['universities'][0]['abbr_name'], courses_data)]

courses_df['categories'] = [*map(lambda course_data: course_data['category-ids'], courses_data)]


# In[66]:

query = courses_df[courses_df['categories'].map(lambda x: 'cs' in str(x))]
#query


# In[64]:

def map_ids_names(ids_array, df, object_name):
    names_array = []
    for object_id in ids_array:
        try:
            names_array.append(df.loc[object_id][object_name])
        except:
            continue
    return names_array


map_ids_names([4,5,15,16], categories_df, 'category_name')


courses_df['categories_name'] = courses_df.apply(lambda row: map_ids_names(row['categories'], categories_df, 'category_name'), axis=1)
courses_df['universities_name'] = courses_df.apply(lambda row: map_ids_names(row['universities'], universities_df, 'university_name'), axis=1)


# In[ ]:



