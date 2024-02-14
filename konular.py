class Konu:
    def __init__(self):
        self.matematik_konulari = {
            'Logaritma1': 'assets/videos/12/Matematik/Logaritma/Logaritma_1.mp4',
            'Logaritma2': 'assets/videos/12/Matematik/Logaritma/Logaritma_2.mp4',
            'Logaritma3': 'assets/videos/12/Matematik/Logaritma/Logaritma_3.mp4',
            'Logaritma4': 'assets/videos/12/Matematik/Logaritma/Logaritma_4.mp4',
            'Logaritma5': 'assets/videos/12/Matematik/Logaritma/Logaritma_5.mp4',
            'Logaritma6': 'assets/videos/12/Matematik/Logaritma/Logaritma_6.mp4',
            'Cebir1': 'assets/videos/12/Matematik/Cebir/Cebir_1.mp4',
            'Cebir2': 'assets/videos/12/Matematik/Cebir/Cebir_2.mp4',
            'Cebir3': 'assets/videos/12/Matematik/Cebir/Cebir_3.mp4',
            'Cebir4': 'assets/videos/12/Matematik/Cebir/Cebir_4.mp4',
            'Cebir5': 'assets/videos/12/Matematik/Cebir/Cebir_5.mp4',
            'Cebir6': 'assets/videos/12/Matematik/Cebir/Cebir_6.mp4',
            'Trigonometri1': 'assets/videos/12/Matematik/Trigonometri/Trigonometri_1.mp4',
            'Trigonometri2': 'assets/videos/12/Matematik/Trigonometri/Trigonometri_2.mp4',
            'Trigonometri3': 'assets/videos/12/Matematik/Trigonometri/Trigonometri_3.mp4',
            'Trigonometri4': 'assets/videos/12/Matematik/Trigonometri/Trigonometri_4.mp4',
            'Trigonometri5': 'assets/videos/12/Matematik/Trigonometri/Trigonometri_5.mp4',
            'Trigonometri6': 'assets/videos/12/Matematik/Trigonometri/Trigonometri_6.mp4'
        }
    
    def konu_yolla(self, konu_ad):
        return self.matematik_konulari[konu_ad]