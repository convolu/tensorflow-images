import tensorflow as tf

from inputPathUtils import get_all_categories, get_all_image_paths


if __name__ == "__main__":

    allFiles = [z for k in get_all_categories() for z in get_all_image_paths(k)]
    allFilesLabels = [k for k in get_all_categories() for z in get_all_image_paths(k)]

    inputFilesProducer = tf.train.string_input_producer(allFiles)

    reader = tf.WholeFileReader()

    keyRead, valueRead = reader.read(inputFilesProducer)

    input_image = tf.image.decode_jpeg(valueRead)

    resized_image = tf.image.resize_image_with_crop_or_pad(input_image, 299, 299)

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        for k in allFiles:
            resized_image_evaluated = resized_image.eval()
            print(resized_image_evaluated)

        coord.request_stop()
        coord.join(threads)

    print("DONE")
