Dear Xue-san,
I tried to improve the code but it was much complicated than I thought.The following code may help but still needs some work.

----------import pandas as pd
import numpy as np

# Create a 4x4 random dataframe
random_matrix = np.random.rand(4, 4)
df = pd.DataFrame(random_matrix, columns=['A', 'B', 'C', 'D'])

# Custom function to calculate the sum, difference, and product of the exponential values of b and c
def calculate_sum_diff_product(b, c):
    """
    This function takes two numbers (b and c) as input, calculates their exponential values,
    and returns the sum, difference, and product of these exponential values.
    """
    b_exp = np.exp(b)
    c_exp = np.exp(c)
    return b_exp + c_exp, b_exp - c_exp, b_exp * c_exp

# Store values in the new columns
df['E'], df['F'], df['G'] = zip(*df.apply(lambda row: calculate_sum_diff_product(row['B'], row['C']), axis=1))
--------


--
******************************************************橋本 佑介東北大学　研究推進・支援機構　知の創出センター特任准教授／URA　データマネージャー〒980-8577　仙台市青葉区片平2-1-1
TEL: 022-217-5973 FAX: 022-217-6097E-mail: yusuke.hashimoto.b8@tohoku.ac.jp
URL: www.tfc.tohoku.ac.jp******************************************************Yusuke Hashimoto Specially Appointed Associate Professor/URA (Ph.D.)Data ManagerTohoku Forum for CreativityOrganization for Research PromotionTohoku University2-1-1 Katahira, Aoba-ku, Sendai, Miyagi, Japan 980-8577TEL: 022-217-5973 FAX: 022-217-6097E-mail: yusuke.hashimoto.b8@tohoku.ac.jp
URL: www.tfc.tohoku.ac.jp******************************************************