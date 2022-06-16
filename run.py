from src.main import App


if __name__ == '__main__':
    app = App(['data_Soruce_1.xml', 'data_Source_2.xml', 'data_Source_3.json'])
    app.compare(
        save_to='data/Results.json',
        inaccurate_word_comparison=False  # Very heavy operation
    )
