import requests
from .models import ArrInstance, UnmonitorRule

def setup_scheduled_tasks(app):
    from apscheduler.triggers.interval import IntervalTrigger
    
    @app.cli.command('sync-arrs')
    def sync_arrs():
        with app.app_context():
            instances = ArrInstance.query.all()
            for instance in instances:
                sync_instance(instance)
    
    def sync_instance(instance):
        # Get all items from the ARR instance
        items = get_arr_items(instance)
        rules = UnmonitorRule.query.filter_by(arr_instance_id=instance.id).all()
        
        for item in items:
            for rule in rules:
                if (item['qualityProfile'] == rule.quality_profile and 
                    any(rg in item.get('releaseGroup', '') for rg in rule.release_groups)):
                    unmonitor_item(instance, item['id'])
    
    def get_arr_items(instance):
        endpoint = f"{instance.url}/api/v3/{'movie' if instance.arr_type == 'radarr' else 'series'}"
        headers = {'X-Api-Key': instance.api_key}
        response = requests.get(endpoint, headers=headers)
        return response.json()
    
    def unmonitor_item(instance, item_id):
        endpoint = f"{instance.url}/api/v3/{'movie' if instance.arr_type == 'radarr' else 'series'}/{item_id}"
        headers = {'X-Api-Key': instance.api_key}
        data = {'monitored': False}
        requests.put(endpoint, headers=headers, json=data)
    
    # Schedule periodic sync for each instance
    instances = ArrInstance.query.all()
    for instance in instances:
        scheduler.add_job(
            sync_instance,
            trigger=IntervalTrigger(seconds=instance.sync_interval),
            args=[instance],
            id=f'sync_{instance.id}'
        )