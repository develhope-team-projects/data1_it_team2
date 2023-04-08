import seaborn as sns
import matplotlib.pyplot as plt
from typing import Literal
import numpy as np
import pandas as pd

class DataVisualizer:

    def __init__(self, library: Literal["seaborn", "matplotlib"] = 'seaborn', style: Literal["darkgrid","whitegrid","dark","white","ticks",False] = False):
        self.library = library
        if style:
            sns.set_theme(style=style)

    def pipeline(self, df, df_all):
        if self.library == 'seaborn':
            self.barh_by_grouping(df, column="Rating", group_by="Category", agg='sum')
            self.scatter_plot(df, 'Installs', 'Reviews')
            self.countplot(df, var='Category', hue='Type')
            self.grouped_rating(df, ["Category", "Type"], "Rating")                          #average Rating devided in free and paid Apps for each Category
            self.grouped_rating(df, "Category", "Rating")                                    #average Rating per Category
            self.popularity_score(df)                                                        #top 10 Apps by Popularity (Rating*Installs)
            self.rating_counter(df, "Rating", "Category")                                    #number of Apps in each Category for each Rating range
            self.rating_counter(df, "Rating", "Type")                                        #number of Apps in each Type (free, paid) for each Rating range
            self.growth_trend(df)
            self.correlation_heatmap(df)
            self.sent_category_hbar(df_all)

        elif self.library == 'matplotlib':
            self.barh_by_grouping(df, column="Rating", group_by="Category", agg='sum')
            self.scatter_plot(df, 'Installs', 'Reviews')
            self.countplot(df, var='Category', hue='Type')
            self.grouped_rating(df, ["Category", "Type"], "Rating")                          #average Rating devided in free and paid Apps for each Category
            self.grouped_rating(df, "Category", "Rating")                                    #average Rating per Category
            self.popularity_score(df)                                                        #top 10 Apps by Popularity (Rating*Installs)
            self.rating_counter(df, "Rating", "Category")                                    #number of Apps in each Category for each Rating range
            self.rating_counter(df, "Rating", "Type") 
            self.growth_trend(df)
            self.correlation_heatmap(df)
            self.sent_category_hbar(df_all)


# Creates a horizontal bar chart for a column in a dataframe grouped by another column 
# using the specified aggregation function.
    def barh_by_grouping(self, df, column, group_by, agg):
        data = df[[group_by, column]].groupby(by=group_by).agg(agg).reset_index()
        
        fig, ax = plt.subplots(figsize=(15, 6))

        if self.library == "seaborn":
            #FYI Seaborn e matplotlib order opposite ways
            sns.barplot(data=data.sort_values(by=column, ascending=False), 
                        y=group_by,
                        x=column,
                        color="b")
            plt.title(f'{column} by {group_by}')
            plt.savefig('./database/output/graphs/barplot_sns.png')
            plt.show()

        else:
            # FYI Seaborn e matplotlib order opposite ways
            data = df[[group_by, column]].groupby(by=group_by).agg(agg).reset_index().sort_values(by=column, ascending=True) 

            ax.barh(y=group_by, width=column, data=data)
            
            ax.set(title = f'{column} by {group_by}',
                    xlabel = column,
                    ylabel= group_by)
            plt.savefig('./database/output/graphs/barplot_mat.png')
            plt.show()



    def countplot(self, df, var:str, hue:str=None, orientation: Literal['orizzontal', 'vertical'] = None):
        """Displays a countplot for every unique value in var, divided by hue if it is specified.
        
        Args:
            df: DataFrame
                Dataset for plotting
            var: str
                Name of a variable to plot
            hue: str, optional
                Name of a variable in which splitting the data for each var entry
                in different bars
            orientation: str, optional
                Allows to specify the orientation of the graph. If not given the orientation
                is decided based on the number of unique values in var.
        Returns: Display graph.             
        """
        fig, ax = plt.subplots()
        plt.subplots_adjust(left= 0.3)

        if not orientation:
            orientation = 'orizzontal' if (len(df[var].unique()) > 5) else 'vertical'

        if orientation == 'vertical':
            if not hue:
                if self.library == 'seaborn':
                    sns.countplot(x=data.items, color='steelblue', order=df[var].value_counts().index)
                else:
                    data = df[var].value_counts().sort_values(ascending=True)
                    plt.bar(x=data.index, height=data.values, color='steelblue')
            else:
                if self.library == 'seaborn':
                    sns.countplot(x=df[var], hue=df[hue], order=df[var].value_counts().index)
                else:
                    data = df.groupby(by=[var, hue])[var, hue].size().unstack(fill_value=0)
                    data = data.sort_values(by=list(data.columns)[0], ascending=False)

                    x = np.arange(len(data.index))
                    width = 0.50 # Width of bars
                    multiplier = 0
                    for attribute, measurment in data.items():
                        offset = width * multiplier
                        bar = ax.bar(x + offset, measurment, width, label=attribute)
                        ax.bar_label(bar, padding=3)
                        multiplier += 1

                    ax.set_xticks(x + width, data.index)
                    

        else:
            if not hue:
                if self.library == 'seaborn':
                    sns.countplot(y=df[var], color='steelblue', order=df[var].value_counts().index)
                else:
                    data = df['Category'].value_counts(ascending=True)
                    plt.barh(y=data.index, width=data.values,color='steelblue')
            else:
                if self.library == 'seaborn':
                    sns.countplot(y=df[var], hue=df[hue], order=df[var].value_counts().index)
                else:
                    data = df.groupby(by=[var, hue])[var, hue].size().unstack(fill_value=0)
                    data = data.sort_values(by=list(data.columns)[0])

                    y = np.arange(len(data.index))
                    height = 0.50 # height of bars
                    multiplier = 0
                    for attribute, measurment in data.items():
                        offset = height * multiplier
                        bar = ax.barh(y + offset, measurment, height, label=attribute)
                        ax.bar_label(bar, padding=3)
                        multiplier += 1

                    ax.set_yticks(y + height, data.index)
                    ax.set(title=f'Number of apps with for each {var} value')

        plt.savefig('./database/output/graphs/countplot_mat.png')
        plt.show()

        
# Creates a scatter plot for two numerical variables in a dataframe.
    def scatter_plot(self, df, col1, col2): 
        def rho(col1, col2):
            r = np.corrcoef(col1, col2)
            return r[0,1]
        
        x = df[col1]
        y = df[col2]

        if self.library == "seaborn":
            sns.regplot(x=x, y=y, data=df)
            plt.title(f"Pearson's correlation coefficient: {rho(x, y)}")
            plt.xlabel(f'Number of {col1}')
            plt.ylabel(f'Total {col2}')
            plt.savefig('./database/output/graphs/scatterplot_sns.png')
            plt.show()

        else:
            plt.plot(x, y, 'o', color='steelblue')
            m, b = np.polyfit(x, y, 1)
            plt.plot(x, m*x+b, color='steelblue')      
            plt.title(f"Pearson's correlation coefficient: {rho(x, y)}")
            plt.xlabel(f'Number of {col1}')
            plt.ylabel(f'Total {col2}')
            plt.savefig('./database/output/graphs/scatterplot_mat.png')
            plt.show()


# Creates a bar chart for the mean, maximum, and minimum rating of a column in a dataframe grouped by another column.
    def grouped_rating(self, df, by: Literal["Category", "Type"], column, n= None, ascending= False):
    
        df_group = df.groupby(by= by)[column].agg(["mean", "max", "min"]).sort_values(["mean", "max", "min"], ascending= [ascending, ascending, ascending]).head(n)

        fig, ax = plt.subplots(figsize= (16, 8))

        if self.library == "seaborn":
            if type(by) != list:
                
                sns.barplot(data= df_group, x= df_group.index, y= "max", color= "g", label= "Max")
                sns.barplot(data= df_group, x= df_group.index, y= "mean", color= "r", label= "Average")
                sns.barplot(data= df_group, x= df_group.index, y= "min", color= "b", label= "Min")
                ax.set_xticklabels(ax.get_xticklabels(), rotation="vertical")
                ax.set(xlabel= by, ylabel= column)
                ax.legend() 
                ax.set_title(f"Rating by {by}")   
                plt.savefig('./database/output/graphs/Rating_distribution_by_category_sns.png')              
            else:
                df_group = df.groupby(by)[column].mean().unstack().sort_values(["Free", "Paid"], ascending = [ascending, ascending]).reset_index().head(n)
                df_melted = pd.melt(df_group, id_vars= "Category", var_name='Type', value_name='Rating')
                sns.barplot(x= "Category", y= "Rating", data=df_melted, hue= "Type", palette= ["blue", "orange"])
                ax.set_ylabel("Rating")
                ax.set_xticklabels(df_melted.Category.unique(), rotation=65)
                ax.set_title("Average Rating of free and paid Apps in each Category")
                ax.legend()
                plt.savefig('./database/output/graphs/Type_distribution_by_category_sns.png')
            
        else:   
            if type(by) != list:
                plt.bar(df_group.index, df_group["max"], color= "g", label='Max')
                plt.bar(df_group.index, df_group["mean"], color= "r", label='Average')
                plt.bar(df_group.index, df_group["min"], color= "b", label='Min')
                plt.legend() 
                plt.ylabel("Rating")
                plt.xticks(rotation= "vertical")
                plt.title(f"Rating by {by}") 
                plt.savefig('./database/output/graphs/Rating_distribution_by_category_sns.png')

            else:
                df_group = df.groupby(by)[column].mean().unstack().sort_values(["Free", "Paid"], ascending = [ascending, ascending]).head(n)
                bar_width = 0.35
                x = np.arange(len(df_group.index))
                y_free = df_group.Free.fillna(0).values
                y_paid = df_group.Paid.fillna(0).values                
                plt.bar(x - bar_width / 2, y_free, bar_width, color= "steelblue", label="Free")
                plt.bar(x + bar_width / 2, y_paid, bar_width, color= "orange", label="Paid")
                plt.ylabel("Rating")
                plt.xticks(x, df_group.index, rotation= 65)
                plt.title("Average Rating of free and paid Apps in each Category")
                plt.legend()
                plt.savefig('./database/output/graphs/Type_distribution_by_category_mat.png')
                
        plt.show()
        

# Calculates the popularity score for each app in a dataframe based on its rating and number
# of installs, and creates a bar chart for the top 10 apps by popularity score.
    def popularity_score(self, df, n= 10, ascending= False, all_info= False, free= "all"):
        df_copy = df.copy()
        df_copy["Popularity"] = round(df_copy.Installs * df_copy.Rating / (int(str(max(df_copy.Installs))[:-3]) if len(str(max(df.Installs))) > 7 else 10), 4)

        if free != "all":
            if free == True:
                df_popularity = df_copy[df_copy["Type"] == "Free"].sort_values(by= ["Popularity", "Installs", "Rating"], ascending= [ascending, ascending, ascending])[df_copy.columns if all_info else ["App","Popularity"]].head(n)
            else:
                df_popularity = df_copy[df_copy["Type"] == "Paid"].sort_values(by= ["Popularity", "Installs", "Rating"], ascending= [ascending, ascending, ascending])[df_copy.columns if all_info else ["App", "Popularity"]].head(n)
        else:
            df_popularity = df_copy.sort_values(by= ["Popularity", "Installs", "Rating"], ascending= [ascending, ascending, ascending])[df_copy.columns if all_info else ["App", "Popularity"]].head(n)
        
        fig, ax = plt.subplots(figsize= (16, 8))
        
        if self.library == "seaborn":
            sns.barplot(x= df_popularity["App"], y= df_popularity["Popularity"], color='steelblue')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=25)
            ax.set(xlabel= "Apps", ylabel= f"Popularity (Installs*Rating/{int(str(max(df.Installs))[:-3]) if len(str(max(df.Installs))) > 7 else 10})")
            ax.set_title("Top 10 Apps by Popularity")
            plt.savefig('./database/output/graphs/popularity_rating_sns.png')
            
        else:
            plt.bar(df_popularity["App"], df_popularity["Popularity"])
            plt.xticks(rotation= 25)
            plt.xlabel("Apps")
            plt.ylabel(f"Popularity (Installs*Rating/{int(str(max(df.Installs))[:-3]) if len(str(max(df.Installs))) > 7 else 10})")
            plt.title("Top 10 Apps by Popularity")
            plt.savefig('./database/output/graphs/popularity_rating_mat.png')
        plt.show()


# Creates a bar chart for the number of apps in each rating range divided by a categorical 
# variable such as category or type.    
    def rating_counter(self, df, column, by: Literal["Category", "Type"], n= None, ascending= False):

        data = df.groupby(by= by)[column].apply(lambda x: pd.cut(x, bins= [1,2,3,4,5]).value_counts()).unstack()
        
        fig, ax = plt.subplots(figsize= (16, 8))

        if self.library == "seaborn":
            data.columns = ["1-2", "2-3", "3-4", "4-5"]  

            if by == "Category":    
                data = data[["4-5", "3-4", "2-3", "1-2"]]
                data = data.sort_values(by= ["4-5", "3-4", "2-3", "1-2"], ascending= [ascending,ascending,ascending,ascending])
                data_melted = data.reset_index().melt(id_vars= by, var_name= "Rating", value_name= "App Count")
                sns.barplot(x= by, y= "App Count", data= data_melted, hue= "Rating")
                ax.set_xticklabels(ax.get_xticklabels(), rotation= "vertical")
                ax.set(xlabel= "Categories", ylabel= "App Count")   
                ax.set_title(f"Number of Apps in each Rating range devided by {by}")
                plt.savefig('./database/output/graphs/rating_counter_category_sns.png')   
                plt.show()  
            elif "Type" in by:
                data.columns = ["4-5", "3-4", "2-3", "1-2"]

                data = data.sort_values(by= ["4-5", "3-4", "2-3", "1-2"], ascending= [ascending,ascending,ascending,ascending])
                data_melted = data.reset_index().melt(id_vars= by, var_name= "Rating", value_name= "App Count")
                sns.barplot(x= by, y= "App Count", data= data_melted, hue= "Rating")
                ax.set_xticklabels(ax.get_xticklabels(), rotation= "vertical")
                ax.set(xlabel= "Categories", ylabel= "App Count")   
                ax.set_title(f"Number of Apps in each Rating range devided by {by}")
                plt.savefig('./database/output/graphs/rating_counter_type_sns.png')   
                plt.show()  
            
        else:
            if "Category" in by:
                data.columns = ["1-2", "2-3", "3-4", "4-5"]
                data = data.sort_values(by= ["4-5", "3-4", "2-3", "1-2"], ascending= [ascending,ascending,ascending,ascending])
                x = np.arange(df[by].nunique())*1.75
                x1 = data["4-5"]
                x2 = data["3-4"]
                x3 = data["2-3"]
                x4 = data["1-2"]
                    
                plt.bar(x - (9*0.1) / 2, x1, 0.3, label= "4-5")
                plt.bar(x - (3*0.1) / 2, x2, 0.3, label= "3-4")
                plt.bar(x + (3*0.1) / 2, x3, 0.3, label= "2-3")
                plt.bar(x + (9*0.1) / 2, x4, 0.3, label= "1-2")
                plt.xticks(x, df[by].unique(), rotation= "vertical")
                plt.ylabel("App Count")
                plt.legend()
                plt.title(f"Number of Apps in each Rating range devided by {by}")
                plt.savefig('./database/output/graphs/rating_counter_category_mat.png')   
                plt.show() 
            elif "Type" in by:
                data.columns = ["4-5", "3-4", "2-3", "1-2"]
                 
                data = data.sort_values(by= ["4-5", "3-4", "2-3", "1-2"], ascending= [ascending,ascending,ascending,ascending])
                x = np.arange(df[by].nunique())*1.75
                x1 = data["4-5"]
                x2 = data["3-4"]
                x3 = data["2-3"]
                x4 = data["1-2"]
                    
                plt.bar(x - (9*0.1) / 2, x1, 0.3, label= "4-5")
                plt.bar(x - (3*0.1) / 2, x2, 0.3, label= "3-4")
                plt.bar(x + (3*0.1) / 2, x3, 0.3, label= "2-3")
                plt.bar(x + (9*0.1) / 2, x4, 0.3, label= "1-2")
                plt.xticks(x, df[by].unique(), rotation= "vertical")
                plt.ylabel("App Count")
                plt.legend()
                plt.title(f"Number of Apps in each Rating range devided by {by}")
                plt.savefig('./database/output/graphs/rating_counter_type_mat.png')   
                plt.show()  


# Creates a line chart for the number of apps updated each year in different categories.
    def growth_trend(self, df):

        df = df[['App', 'Category', 'Last Updated']]
        #1 Selezione categorie da mostrare nel grafico
        categories = ['Entertainment', 'Business', 'Family', 'Finance', 'Productivity']
        df_main = df[df['Category'].isin(categories)]
        df_main.loc[:, 'Last Updated'] = pd.to_datetime(df['Last Updated'])
        #2 group by anno e conteggio numero app per categoria per ogni anno
        grouped = df_main.groupby([df_main['Last Updated'].dt.year, 'Category'])['Category'].count()
        #3 Riempi i valori nan con 0
        trend = grouped.unstack(level=1, fill_value=0)

        # Ripeti i passaggi 1, 2, 3 per creare un altro dataframe che possa computare la media delle categorie mancanti
        df_else = df[~df['Category'].isin(categories)]
        df_else.loc[:, 'Last Updated'] = pd.to_datetime(df_else['Last Updated'])
        grouped_else = df_else.groupby([df_else['Last Updated'].dt.year, 'Category'])['Category'].count()
        trend_else = grouped_else.unstack(level=1, fill_value=0)
        trend_else_mean = trend_else.mean(axis=1)

        # Aggiungi la media ricavata al dataframe principale
        trend['Average of other categories'] = trend_else_mean

        # Creazione plot 
        if self.library=='seaborn':
            sns.lineplot(data=trend)
            plt.title('Growth of number of Apps by Category Over Time')
            plt.xlabel('Year')
            plt.ylabel('Average Number of Apps')
            plt.savefig('./database/output/graphs/growth_trend_sns.png')
        
        else:
            trend.plot(kind='line', figsize=(10,5))
            plt.title('Growth of number of Apps by Category Over Time')
            plt.xlabel('Year')
            plt.ylabel('Average Number of Apps')
            plt.savefig('./database/output/graphs/growth_trend_mat.png')
        plt.show()


# Creates a heatmap for the correlation matrix of a dataframe.
    def correlation_heatmap(self, df):
        std_df = df.corr()
        std_df = std_df.drop(columns=['Unnamed: 0'], index=['Unnamed: 0'])
        
        if self.library=='seaborn':
            plt.figure(figsize = (15,6))
            sns.heatmap(std_df, annot=True)
            plt.title('Correlation heatmap')
            plt.savefig('./database/output/graphs/correlation_heatmap_sns.png')
        else:
            # Create a colormap
            cmap = plt.get_cmap('magma')

            # Plot the matrix
            fig, ax = plt.subplots(figsize=(15, 6))
            im = ax.imshow(std_df, cmap=cmap, extent=[0, len(std_df.columns), 0, len(std_df.columns)], origin='lower')

            # Set ticks and labels
            xticks = np.arange(0.5, len(std_df.columns), 1)
            yticks = np.arange(0.5, len(std_df.columns), 1)
            ax.set_xticks(xticks, minor=False)
            ax.set_yticks(yticks, minor=False)
            ax.set_xticklabels(std_df.columns, fontsize=15, rotation=65)
            ax.set_yticklabels(std_df.columns, fontsize=15)

            # Set colorbar
            cbar = fig.colorbar(im, ax=ax, orientation='vertical')
            cbar.ax.tick_params(labelsize=15, rotation=90)  # Set font size and rotation of colorbar labels

            # Loop over data dimensions and create text annotations
            for i in range(len(std_df.columns)):
                for j in range(len(std_df.columns)):
                    text = ax.text(j+0.5, i+0.5, round(std_df.to_numpy()[i, j], 2),
                                ha="center", va="center", color="white", fontsize=12)
            plt.title('Correlation heatmap')
            plt.savefig('./database/output/graphs/correlation_heatmap_mat.png')
        plt.show()
        

# Creates a bar chart for the average sentiment score of apps in each category.
    def sent_category_hbar(self, df_all):
        data = df_all.groupby("Category")["sentiment score"].mean().sort_values(ascending= False)

        fig, ax = plt.subplots(figsize= (16, 8))

        if self.library == "seaborn":
            x = np.arange(len(data.index))
            width = 0.35
            sns.barplot(x= data.index.astype(str), y= data.values, data= data, order= data.sort_values(ascending= False), color='b')
            ax.set_xticks(x + width, data.index, rotation= "vertical")
            ax.set(xlabel= "Categories", ylabel= "Sentiment Score")
            plt.savefig('./database/output/graphs/sentiment_by_category_sns.png')

        else:
            data = data.sort_values(ascending= False)
            plt.bar(data.index, data.values)
            plt.xticks(rotation= 35, ha= "right", fontsize= 8)
            plt.ylabel("Avg Sentiment")
            plt.subplots_adjust(bottom= 0.25)
            plt.title("Average sentiment per Category")
            plt.savefig('./database/output/graphs/sentiment_by_category_mat.png')

        plt.show()