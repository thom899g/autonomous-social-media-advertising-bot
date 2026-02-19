from typing import Dict, Optional, List
import logging
from datetime import datetime
from .ad_creator import AdCreator
from .audience_targeter import AudienceTargeter
from .bid_optimizer import BidOptimizer
from .performance_analyzer import PerformanceAnalyzer

class CampaignManager:
    def __init__(self):
        self.campaigns: Dict[str, Dict] = {}
        self.last_updated = datetime.now()
        
    def create_campaign(self, platform: str, config: Dict) -> str:
        """Creates a new advertising campaign on the specified platform."""
        try:
            # Validate inputs
            if not isinstance(config, dict):
                raise ValueError("Campaign configuration must be a dictionary.")
            
            ad_creator = AdCreator.get_instance(platform)
            audience_targeter = AudienceTargeter.get_instance()
            bid_optimizer = BidOptimizer.get_instance(platform)
            
            # Generate ad content
            ad_content = ad_creator.create_ad(config)
            
            # Target audience
            audience = audience_targeter.target_audience(config['targeting'])
            
            # Set initial bids
            bid_optimizer.set_bids(audience.size)
            
            # Store campaign details
            campaign_id = f"{platform}_camp_{len(self.campaigns) + 1}"
            self.campaigns[campaign_id] = {
                'id': campaign_id,
                'platform': platform,
                'config': config,
                'status': 'running',
                'start_time': datetime.now(),
                'performance': {},
                'errors': []
            }
            
            logging.info(f"Campaign {campaign_id} created on {platform}.")
            return campaign_id
            
        except Exception as e:
            logging.error(f"Failed to create campaign: {str(e)}")
            raise
        
    def optimize_campaign(self, campaign_id: str) -> None:
        """Optimizes the specified campaign based on performance data."""
        try:
            if campaign_id not in self.campaigns:
                raise ValueError(f"Campaign {campaign_id} does not exist.")
                
            # Get performance analyzer
            analyzer = PerformanceAnalyzer.get_instance()
            
            # Analyze current performance
            metrics = analyzer.analyze_campaign(campaign_id)
            
            # Optimize bids and targeting
            bid_optimizer = BidOptimizer.get_instance(self.campaigns[campaign_id]['platform'])
            bid_optimizer.adjust_bids(metrics)
            
            # Update campaign status
            self.campaigns[campaign_id]['performance'] = metrics
            logging.info(f"Campaign {campaign_id} optimized. New performance metrics: {metrics}.")
            
        except Exception as e:
            logging.error(f"Optimization failed for campaign {campaign_id}: {str(e)}")
            raise
        
    def scale_campaign(self, campaign_id: str, direction: str) -> None:
        """Scales the campaign up or down based on performance."""
        try:
            if campaign_id not in self.campaigns:
                raise ValueError(f"Campaign {campaign_id} does not exist.")
                
            # Check current status
            current_status = self.campaigns[campaign_id]['status']
            
            if direction == 'up':
                new_status = 'scaling_up'
            elif direction == 'down':
                new_status = 'scaling_down'
            else:
                raise ValueError("Direction must be either 'up' or 'down'.")
                
            # Update campaign status
            self.campaigns[campaign_id]['status'] = new_status
            logging.info(f"Campaign {campaign_id} scaling {direction}. New status: {new_status}.")
            
        except Exception as e:
            logging.error(f"Scaling failed for campaign {campaign_id}: {str(e)}")
            raise
        
    def stop_campaign(self, campaign_id: str) -> None:
        """Stops the specified campaign."""
        try:
            if campaign_id not in self.campaigns:
                raise ValueError(f"Campaign {campaign_id} does not exist.")
                
            # Delete campaign data
            del self.campaigns[campaign_id]
            logging.info(f"Campaign {campaign_id} stopped successfully.")
            
        except Exception as e:
            logging.error(f"Failed to stop campaign {campaign_id}: {str(e)}")
            raise
        
    def get_campaign_status(self, campaign_id: str) -> Dict:
        """Returns the status of the specified campaign."""
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} does not exist.")
            
        return self.campaigns[campaign_id]