from keras.datasets import cifar100
import keras
import numpy as np

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

# データセット抽出用の関数
def select_data(label_list):
    # row data load
    (x_train, y_train), (x_test, y_test) = cifar100.load_data()

    # label name : label num
    label_name_dict ={'apple': 0,
 'aquarium_fish': 1,
 'baby': 2,
 'bear': 3,
 'beaver': 4,
 'bed': 5,
 'bee': 6,
 'beetle': 7,
 'bicycle': 8,
 'bottle': 9,
 'bowl': 10,
 'boy': 11,
 'bridge': 12,
 'bus': 13,
 'butterfly': 14,
 'camel': 15,
 'can': 16,
 'castle': 17,
 'caterpillar': 18,
 'cattle': 19,
 'chair': 20,
 'chimpanzee': 21,
 'clock': 22,
 'cloud': 23,
 'cockroach': 24,
 'couch': 25,
 'crab': 26,
 'crocodile': 27,
 'cup': 28,
 'dinosaur': 29,
 'dolphin': 30,
 'elephant': 31,
 'flatfish': 32,
 'forest': 33,
 'fox': 34,
 'girl': 35,
 'hamster': 36,
 'house': 37,
 'kangaroo': 38,
 'keyboard': 39,
 'lamp': 40,
 'lawn_mower': 41,
 'leopard': 42,
 'lion': 43,
 'lizard': 44,
 'lobster': 45,
 'man': 46,
 'maple_tree': 47,
 'motorcycle': 48,
 'mountain': 49,
 'mouse': 50,
 'mushroom': 51,
 'oak_tree': 52,
 'orange': 53,
 'orchid': 54,
 'otter': 55,
 'palm_tree': 56,
 'pear': 57,
 'pickup_truck': 58,
 'pine_tree': 59,
 'plain': 60,
 'plate': 61,
 'poppy': 62,
 'porcupine': 63,
 'possum': 64,
 'rabbit': 65,
 'raccoon': 66,
 'ray': 67,
 'road': 68,
 'rocket': 69,
 'rose': 70,
 'sea': 71,
 'seal': 72,
 'shark': 73,
 'shrew': 74,
 'skunk': 75,
 'skyscraper': 76,
 'snail': 77,
 'snake': 78,
 'spider': 79,
 'squirrel': 80,
 'streetcar': 81,
 'sunflower': 82,
 'sweet_pepper': 83,
 'table': 84,
 'tank': 85,
 'telephone': 86,
 'television': 87,
 'tiger': 88,
 'tractor': 89,
 'train': 90,
 'trout': 91,
 'tulip': 92,
 'turtle': 93,
 'wardrobe': 94,
 'whale': 95,
 'willow_tree': 96,
 'wolf': 97,
 'woman': 98,
 'worm': 99}

    # データ抽出 & ラベルデータ成形
    X_train = []
    class_num = len(label_list)
    for e,i in enumerate(label_list):
        label_num = label_name_dict[i]
        one_hot_array = keras.utils.to_categorical(e, class_num)

        if X_train == []:
            X_train = x_train[np.where(y_train==label_num)[0]]
            X_test = x_test[np.where(y_test==label_num)[0]]
            Y_train = np.tile(one_hot_array,(len(y_train[np.where(y_train==label_num)[0]]),1))
            Y_test = np.tile(one_hot_array, (len(y_test[np.where(y_test==label_num)[0]]),1))
        else:
            X_train = np.append(X_train,x_train[np.where(y_train==label_num)[0]],axis=0)
            X_test = np.append(X_test,x_test[np.where(y_test==label_num)[0]],axis=0)
            Y_train = np.append(Y_train,np.tile(one_hot_array,(len(y_train[np.where(y_train==label_num)[0]]),1)),axis=0)
            Y_test = np.append(Y_test,np.tile(one_hot_array,(len(y_test[np.where(y_test==label_num)[0]]),1)),axis=0)

    return ((X_train,Y_train),(X_test, Y_test))
