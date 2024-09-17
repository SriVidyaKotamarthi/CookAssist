
import os
import pandas as pd
import decimal
from recipe import Recipe


class RecipeService:
    def __init__(self, 
        file_path: str
    ) -> None:
        self.file_path = file_path
        self.recipes_master_data: pd.DataFrame
        self.ingredients_recipes_master_data: pd.DataFrame
        self.recipes = []
        self.final_dataframe = pd.DataFrame

    def get_recommended_recipes(self, list_ingreds:list, order_by:str = None):
        # merged_ingreds_file = '100_recipe_prim_merged_ingredients.csv'
        # merged_recipes_file = '100_recipe_prim_merged_recipes.csv'
        recipe_with_nutrition_time = '100_Recipes Gaurav.v2.csv'
        # df_merged_ingreds_file_master = pd.read_csv(self.file_path+merged_ingreds_file)
        # df_merged_recipes_file_master = pd.read_csv(self.file_path+merged_recipes_file)
        self.recipes_master_data = pd.read_csv(self.file_path+recipe_with_nutrition_time)
        data = self.recipes_master_data
        # Ing_available = ['Almonds','Tomato','Jaggery','White Chickpeas','Peanuts']
        Ing_available = list_ingreds
        data['Ing_count'] = data['Ingredient'].str.split(',').apply(len)
        data['Primary_ing'] = data['Ingredient'].str.split(',').str[0]
        data['Secondry_ing'] = data['Ingredient'].str.split(',').str[1]
        data['Primary_flag'] = data['Primary_ing'].apply(lambda x: 1 if x in Ing_available else 0)
        data['Secondry_flag'] = data['Secondry_ing'].apply(lambda x: 1 if x in Ing_available else 0)
        for ing in Ing_available:
            data[ing]= data['Ingredient'].str.find(ing,0)
            data[ing] = data[ing].apply(lambda x: 0 if x==-1 else 1)

        ## How many ingredents availabel for each recipie.
        data['Ing_available_count'] = data[Ing_available].sum(axis=1)
        data['% Available'] = data['Ing_available_count']/data['Ing_count']
        data.drop(columns=["Unnamed: 0"], inplace=True)
        # data = data[data['Primary_flag']==1]
        df = data.sort_values(['Primary_flag','% Available','Ing_count'],ascending=False, inplace=False).head(10)
        self.final_dataframe = df[["recipe_shrt_name","total_time","rating","nutrition","URL","Ingredient"]]
        self.final_dataframe.rename(columns = {'recipe_shrt_name':'Recipe',
                        'total_time':'Time(mins)', 
                        'rating':'Rating','nutrition':'Calories',
                        'Ingredient':'Ingredients'}, inplace = True)
        if order_by != None:
            if order_by == 'Time' :
                self.final_dataframe.sort_values('Time(mins)',ascending=True, inplace=True)
            else:
                self.final_dataframe.sort_values(order_by,ascending=False, inplace=True)

        self.final_dataframe['Recipe'] = self.final_dataframe.apply(lambda x: self.make_clickable(x['URL'],x['Recipe']), axis=1)
        self.final_dataframe.drop(columns=["URL"], inplace=True)
        self.final_dataframe.reset_index(drop=True, inplace=True)
        print(self.final_dataframe)

    def load_recipes_list(self, df: pd.DataFrame):

        for index, row in df.iterrows():
            recipe_obj = Recipe()
            recipe_obj.short_name = row['Recipe']
            recipe_obj.total_time = row['Time(mins)']
            recipe_obj.calories = row['Calories']
            recipe_obj.rating = row['Rating']
            recipe_obj.URL = row['Ingredients']
            self.recipes.append(recipe_obj)

    def make_clickable(self,link, text):
        return f'<a target="_blank" href="{link}">{text}</a>'
