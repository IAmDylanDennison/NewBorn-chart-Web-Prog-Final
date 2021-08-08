
import dataset

if __name__ == "__main__":
    chart_db = dataset.connect('sqlite:///chart.db')
    chart = chart_db.get_table('chart')
    chart.drop()
    chart = chart_db.create_table('chart')
    chart.insert_many([
        { 'username' : 'dylan', 'time' : '9 am','length' :"15", 'side' : 'right', 'poops' : '1', 'pees' : '1' },
        { 'username' : 'dylan', 'time' : '12 pm','length' :"10", 'side' : 'left', 'poops' : '0', 'pees' : '2' },
        { 'username' : 'dylan', 'time' : '3 pm','length' :"20", 'side' : 'right', 'poops' : '2', 'pees' : '1' },
        

    ])



