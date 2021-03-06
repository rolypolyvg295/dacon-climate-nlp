import wandb

def log_init(setting):
    config_exclude_keys = [
        'project', 'entity', 'device_pref', 'logging', 'tags', 'name', 'is_testing'
    ]

    mode = 'online' if setting.logging else 'disabled'
    wandb.init(
        project=setting.project,
        entity=setting.entity,
        name=setting.name,
        config=setting,
        config_exclude_keys=config_exclude_keys, 
        mode=mode,
        tags=setting.tags,
    )

class Logger:
    def __init__(self, should_log=True):
        self.should_log = should_log

    def reset(self, cur_epoch):
        self.logging_dict = {'epoch': cur_epoch}

    def add_log_item(self, name, value, prefix=''):
        if not self.should_log:
            return

        if prefix == '':
            log_name = name
        else:
            log_name = f'{prefix}_{name}'
        self.logging_dict[log_name] = value

    def add_log_dict(self, dic, prefix=''):
        if not self.should_log:
            return

        for k, v in dic.items():
            self.add_log_item(k, v, prefix=prefix)

    def log(self):
        if not self.should_log:
            return

        wandb.log(self.logging_dict, commit=True)