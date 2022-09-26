from math import isnan, sqrt
from numpy import sort
import pandas as pd
import sys
from genericpath import exists
from os import makedirs

class Features(object):
    def __init__(self, name, values, house_list=None, house_name=None, full_list=None):
        if (house_list == None):
            self.name = name
            self.values = self.get_values(values=values)
        else:
            self.name = name + "_" + house_name
            self.values = self.get_values_house(indexes=house_list, full_list=full_list)
        self.count = self.get_count()
        self.mean = round(self.get_mean(), 6)
        self.std = round(self.get_std(), 6)
        self.min = round(min(self.values), 6)
        self.max = round(max(self.values), 6)
        self.p_25 = round(sort(self.values)[int((self.count/100) * 25)], 6)
        self.p_50 = round(sort(self.values)[int((self.count/100) * 50)], 6)
        self.p_75 = round(sort(self.values)[int((self.count/100) * 75)], 6)
    
    def get_name(self):
        return self.name

    def get_count(self):
        if len(self.values) <= 0:
            self.values.append(0)
        return len(self.values)

    def get_values(self, values):
        ret_values = []
        for i in range(len(values)):
            if (values[i] == "Right"):
                values[i] = 0
            elif (values[i] == "Left"):
                values[i] = 1
            if (isnan(float(values[i]))):
                continue
            ret_values.append(values[i])
        return ret_values

    def get_values_house(self, indexes, full_list):
        ret_values = []
        for i in indexes:
            if (full_list[i] == "Right"):
                full_list[i] = 0
            elif (full_list[i] == "Left"):
                full_list[i] = 1
            elif (isnan(float(full_list[i]))):
                continue
            ret_values.append(full_list[i])
        return ret_values
    
    def get_mean(self):
        mean = 0.0
        for i in range(self.count):
            mean += float(self.values[i])
        return mean/self.count
        
    
    def get_std(self):
        std = 0.0
        for i in range(self.count):
            std += (float(self.values[i]) - self.mean)**2
        std = sqrt(std/self.count)
        return std
    

class DescribeData(object):
    def __init__(self, name_of_dataset):
        self.column_names = ["Hogwarts House","First Name","Last Name","Birthday","Best Hand","Arithmancy",\
                        "Astronomy","Herbology","Defense Against the Dark Arts","Divination","Muggle Studies", \
                        "Ancient Runes","History of Magic","Transfiguration","Potions","Care of Magical Creatures","Charms","Flying"]
        self.houses = ["Ravenclaw", "Gryffindor", "Slytherin", "Hufflepuff"]
        self.features_names = self.column_names[4:]
        self.dataset = name_of_dataset
        self.all_data = self.get_dataframe()                    #dataframe of input_scv
        self.dict_by_columns = self.get_dict_by_columns()       
        self.features = self.features_init()
        self.dataframe = self.create_dataframe(self.features)
        self.dict_by_houses = self.get_dict_by_houses() # {HouseName, [list_of_indexes]}
        self.features_by_houses = self.get_features_by_houses() # {HouseName, [list_of_Features]}

    def features_init(self):
        features = []
        for i in range(len(self.features_names)):
            features.append(Features(name=self.features_names[i], values=self.dict_by_columns[self.features_names[i]]))
        return features

    def get_features_by_houses(self):
        feature_list_Ravenclaw = []
        feature_list_Gryffindor = []
        feature_list_Slytherin = []
        feature_list_Hufflepuff = []
        dict_of_houses = {}
        dict_of_houses[self.houses[0]] = feature_list_Ravenclaw
        dict_of_houses[self.houses[1]] = feature_list_Gryffindor
        dict_of_houses[self.houses[2]] = feature_list_Slytherin
        dict_of_houses[self.houses[3]] = feature_list_Hufflepuff
        for house in dict_of_houses.keys():
            for i in range(len(self.features_names)):
                dict_of_houses[house].append(Features(name=self.features_names[i], values=self.dict_by_columns[self.features_names[i]], \
                                        house_list=self.dict_by_houses[house], house_name=house, full_list=self.all_data[self.features_names[i]].to_list()))
        return dict_of_houses

    def get_dataframe(self):
        df = pd.read_csv(self.dataset, header=0, names=self.column_names)
        return df

    def get_dict_by_columns(self):
        dict_values = {}
        for i in range(len(self.column_names)):
            dict_values[self.column_names[i]] = self.get_list_by_column(self.column_names[i])
        return dict_values

    def get_list_by_column(self, column_name):
        column_list = self.all_data[column_name].to_list()
        return column_list
    
    def create_dataframe(self, list_of_features):
        data = []
        names = ["Вычисления"]
        names = names + self.features_names

        data.append(self.get_count(list_of_features))
        data.append(self.get_mean(list_of_features))
        data.append(self.get_std(list_of_features))
        data.append(self.get_min(list_of_features))
        data.append(self.get_p25(list_of_features))
        data.append(self.get_p50(list_of_features))
        data.append(self.get_p75(list_of_features))
        data.append(self.get_max(list_of_features))
        df = pd.DataFrame(data, columns=names)
        return df
    
    def get_count(self, list_of_features):
        ret_list = []
        ret_list.append("Count")
        for i in list_of_features:
            ret_list.append(i.count)
        return ret_list

    def get_mean(self, list_of_features):
        ret_list = []
        ret_list.append("Mean")
        for i in list_of_features:
            ret_list.append(i.mean)
        return ret_list

    def get_std(self, list_of_features):
        ret_list = []
        ret_list.append("Std")
        for i in list_of_features:
            ret_list.append(i.std)
        return ret_list

    def get_min(self, list_of_features):
        ret_list = []
        ret_list.append("Min")
        for i in list_of_features:
            ret_list.append(i.min)
        return ret_list

    def get_p25(self, list_of_features):
        ret_list = []
        ret_list.append("25%")
        for i in list_of_features:
            ret_list.append(i.p_25)
        return ret_list

    def get_p50(self, list_of_features):
        ret_list = []
        ret_list.append("50%")
        for i in list_of_features:
            ret_list.append(i.p_50)
        return ret_list

    def get_p75(self, list_of_features):
        ret_list = []
        ret_list.append("75%")
        for i in list_of_features:
            ret_list.append(i.p_75)
        return ret_list

    def get_max(self, list_of_features):
        ret_list = []
        ret_list.append("Max")
        for i in list_of_features:
            ret_list.append(i.max)
        return ret_list
    
    def get_dict_by_houses(self):
        index_list_Ravenclaw = []
        index_list_Gryffindor = []
        index_list_Slytherin = []
        index_list_Hufflepuff = []
        dict_of_houses = {}
        dict_of_houses[self.houses[0]] = index_list_Ravenclaw
        dict_of_houses[self.houses[1]] = index_list_Gryffindor
        dict_of_houses[self.houses[2]] = index_list_Slytherin
        dict_of_houses[self.houses[3]] = index_list_Hufflepuff

        for i in range(len(self.all_data["Hogwarts House"])):
            if self.all_data["Hogwarts House"][i] == self.houses[0]:
                index_list_Ravenclaw.append(i)
            elif self.all_data["Hogwarts House"][i] == self.houses[1]:
                index_list_Gryffindor.append(i)
            elif self.all_data["Hogwarts House"][i] == self.houses[2]:
                index_list_Slytherin.append(i)
            elif self.all_data["Hogwarts House"][i] == self.houses[3]:
                index_list_Hufflepuff.append(i)
        return dict_of_houses
    
    def make_describe_csv(self): # показывает общую статистику по всем факультетам
        print(self.dataframe)
        self.dataframe.to_csv('./describe/describe.csv', index=False)
    
    def make_house_feautures(self): # показывает статистику по каждому отдельному факультету
        i = 0
        houses_dataframes = []
        for name in self.houses:
            houses_dataframes.append(self.create_dataframe(self.features_by_houses[name]))
            houses_dataframes[i].to_csv("./describe/houses/{0}_features.csv".format(name))
            i += 1
    
    def make_house_marks(self):
        col_list = self.features_names
        col_list.append(self.column_names[0])
        df = pd.DataFrame(self.all_data, columns=col_list)
        df_list = {}

        for house in self.houses:
            df_list[house] = df[(df[["Hogwarts House"]] == house).all(axis=1)].reset_index(drop=True)
        for house in self.houses:
            df_list[house].to_csv("./describe/house_marks/{0}_marks.csv".format(house))
        col_list.pop()
    
    def make_marks_feautures(self):
        for i in range(len(self.features_names)):
            data = []
            for name in self.houses:
                # print(self.features_names[i])
                data.append(self.features_by_houses[name][i].values)
            df = pd.DataFrame(data, index=self.houses)
            df.reset_index()
            tmp = []
            for k, j in df.iterrows():
                tmp.append(j.to_list())

            data = []
            for x in range(len(tmp[3])):
                new_tmp = []
                for y in range(len(tmp)):
                    new_tmp.append(tmp[y][x])
                data.append(new_tmp)
            data_frame = pd.DataFrame(data, columns=self.houses)
            data_frame.to_csv("./describe/features/{0}.csv".format(self.features_names[i]))

def main():
    if len(sys.argv) != 2:
        print("Usage: python.exe .\describe.py dataset_name")
        exit(0)
    else:
        try:
            with open(sys.argv[1], 'r') as fd:
                fd.close()
        except IOError:
            print("Can't open dataset file")
            exit(0)
        # work with object
        describe_obj = DescribeData(sys.argv[1])
        if exists("./describe/") == False: 
            makedirs("./describe/")
            makedirs("./describe/houses/")
            makedirs("./describe/house_marks/")
            makedirs("./describe/features/")

        #   describe.csv
        describe_obj.make_describe_csv()

        #   house_feautures
        describe_obj.make_house_feautures()

        #   House_marks
        describe_obj.make_house_marks()

        #   Marks_features
        describe_obj.make_marks_feautures()
        return 0

if __name__ == '__main__':
    sys.exit(main())
