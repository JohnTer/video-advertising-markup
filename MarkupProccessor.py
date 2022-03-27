


class MarkupProccessor(object):
    def __init__(self) -> None:
        pass

    def get_sound_video_weight_vector(self, video_weight_vector, sound_weight_vector):
        
        
        sound_video_weight_vector = []
        for weights in video_weight_vector:
            packet_info = {''}

    def get_speech(self, noise_vector_with_weight):
        max_diff = max(noise_vector_with_weight, key=lambda x: x['weight'])
        min_diff = min(noise_vector_with_weight, key=lambda x: x['weight'])
        delta = max_diff['weight'] - min_diff['weight']
        for i in range(len(noise_vector_with_weight)):
            noise_vector_with_weight[i]['weight'] = (noise_vector_with_weight[i]['weight'] - min_diff['weight']) / delta

        return noise_vector_with_weight


