import random
import tensorflow as tf

from inputPathUtils import get_all_categories, get_all_image_paths


def preprocess_image(filename):
    value_read = tf.read_file(filename)
    input_image = tf.image.decode_jpeg(value_read, channels=3)
    return tf.image.resize_image_with_crop_or_pad(input_image, 299, 299)


def get_batched_input(data, batch_size=50):
    data_input_q = tf.train.slice_input_producer(data, shuffle=False)

    data_image = preprocess_image(data_input_q[0])
    data_label = data_input_q[1]

    data_image_batch, data_label_batch = tf.train.batch([data_image, data_label], batch_size=batch_size)
    return data_image_batch, data_label_batch


if __name__ == "__main__":

    allFiles = [z for k in get_all_categories() for z in get_all_image_paths(k)]
    allFilesLabels = [k for k in get_all_categories() for z in get_all_image_paths(k)]

    label_to_number = {label: i for i, label in enumerate(set(allFilesLabels), 1)}
    allFilesLabelsInt = [int(label_to_number[i]) for i in allFilesLabels]

    test_set_size = int(.3 * len(allFiles))
    partitions = [0] * len(allFiles)
    partitions[:test_set_size] = [1] * test_set_size
    random.shuffle(partitions)
    train_images, test_images = tf.dynamic_partition(allFiles, partitions, 2)
    train_labels, test_labels = tf.dynamic_partition(allFilesLabelsInt, partitions, 2)

    # Pipeline
    train_image_batch, train_label_batch = get_batched_input([train_images, train_labels])
    test_image_batch, test_label_batch = get_batched_input([test_images, test_labels])

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        for i in range(30):
            a = train_image_batch.eval()
            print(a)

        coord.request_stop()
        coord.join(threads)

    print("DONE")
