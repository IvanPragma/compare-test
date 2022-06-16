import time
import numpy as np

from src.data_engine import DataEngine
from src.data_structure import Structure
from src.tools import words_same


class App:
    """Receive files paths, compare products."""

    def __init__(self,
                 data_files: list[str],
                 data_dir: str = 'data') -> None:
        self.data_files: list[str] = data_files
        self.data_dir = data_dir

    def compare(self,
                compare_in_source: bool = False,
                save_to: str = 'Results.json',
                inaccurate_word_comparison: bool = False) -> None:
        """Compare files and save result to file.

        If inaccurate_word_comparison is True the program will
        run ~4 times longer.
        """

        products = []
        start = time.time()
        print('Form starts...')
        for i, file in enumerate(self.data_files):
            for product in self.read(file):
                clean_product = \
                    Structure(product, structure_source='.'.join(file.split('.')[:-1])).format(
                    ['source_name', 'name', 'ean_code', 'id']
                )
                products.append(
                    np.array(clean_product)
                )
        products = np.array(products)
        end = time.time()
        print(f'From past in {end-start} seconds')
        
        # Hardest operation I've ever seen xD
        # I think we should use C++ here instead of python
        result = []
        already_processed_products = []
        already_processed_products_count = 0
        prc_max = len(products)
        start = time.time()
        same_products_count = 0
        print(f'Compare starts ({prc_max} products)...')
        for appc, product_1 in enumerate(products):
            this_product_duplicates = []
            for i, product_2 in enumerate(products):
                if i <= appc:
                    continue
                
                if not compare_in_source:
                    if product_1[0] == product_2[0]:
                        continue

                if product_1[2] == product_2[2]:
                    this_product_duplicates.append(list(product_2))
                else:
                    if inaccurate_word_comparison:
                        if words_same(product_1[1], product_2[1]) > 0.7:
                            this_product_duplicates.append(list(product_2))
                    else:
                        if product_1[1] == product_2[1]:
                            this_product_duplicates.append(list(product_2))

            if len(this_product_duplicates) > 1:
                same_products_count += 1
                result.append([list(product_1), *this_product_duplicates])

            if appc % 5 == 0 and appc != 0:
                now = time.time()
                remain_products = prc_max - appc
                prc = round(appc / prc_max * 100, 4)
                print(f'passed {prc}% ({appc}/{prc_max} entries)')
                print('remain:', (now-start)/appc*remain_products, 'seconds')
        end = time.time()
        print(f'Compare past in {end-start} seconds')
        print(f'Found {same_products_count} same products')

        DataEngine.write(save_to, result)

    def read(self, path: str) -> any:
        return DataEngine.read(self.data_dir + '/' + path)
