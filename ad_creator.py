from typing import Dict, Optional
import logging
from .image_generator import ImageGenerator

class AdCreator:
    def __init__(self):
        pass
        
    @classmethod
    def get_instance(cls, platform: str) -> 'AdCreator':
        """Factory method to return the appropriate ad creator instance."""
        if platform == 'facebook':
            from .ad_creators.facebook_ad_creator import FacebookAdCreator as Creator
        elif platform == 'instagram':
            from .ad_creators.instagram_ad_creator import InstagramAdCreator as Creator
        elif platform == 'twitter':
            from .ad_creators.twitter_ad_creator import TwitterAdCreator as Creator
        elif platform == 'google_ads':
            from .ad_creators.google_ads_creator import GoogleAdsCreator as Creator
        else:
            raise ValueError(f"Unsupported platform: {platform}")
            
        return Creator()
        
    def create_ad(self, config: Dict) -> Dict:
        """Creates an ad based on the provided configuration."""
        try:
            # Validate inputs
            if not isinstance(config, dict):
                raise ValueError("Ad configuration must be a dictionary.")
                
            # Generate text content
            text_content = self._generate_text(config['text_template'])
            
            # Generate visual content
            image_path = self._generate_image(config.get('image_options'))
            
            return {
                'platform': self.platform,
                'content': text_content,
                'visual': image_path,
                'cta': config.get('call_to_action'),
                'status': 'generated'
            }
            
        except Exception as e: