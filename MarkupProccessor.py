


class MarkupProccessor(object):
    def __init__(self) -> None:
        pass

    def get_sound_video_weight_vector(self, video_weight_vector, sound_weight_vector):
        
        
        sound_video_weight_vector = []
        for weights in video_weight_vector:
            packet_info = {''}

    def get_score(self, noise_vector_with_weight):
        if not noise_vector_with_weight:
            return []
        max_diff = max(noise_vector_with_weight, key=lambda x: x['weight'])['weight']
        min_diff = min(noise_vector_with_weight, key=lambda x: x['weight'])['weight']
        delta = max_diff - min_diff
        
        
        for i in range(len(noise_vector_with_weight)):
            noise_vector_with_weight[i]['weight'] = (noise_vector_with_weight[i]['weight'] - min_diff) / delta + 1

        return noise_vector_with_weight

    def calculate_ads_score(self, frame_diff_vector, silence_vector):
        def get_silence_weight(diff_element):
            for silence_element in silence_vector:
                time_tuple = silence_element['time']
                if time_tuple[0] <= diff_element['time'] <= time_tuple[1]:
                    return silence_element['weight']
            return 0.01
        
        weight_vector = []
        for diff_element in frame_diff_vector:
            diff_element['weight'] *= get_silence_weight(diff_element)
            weight_vector.append(diff_element)

        return weight_vector




