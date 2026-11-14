import yaml
from .errors import ConfigError

def load_config(file_path):
    # 读取、解析
    try:
        with open(file_path, 'r', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        raise ConfigError(f'找不到文件: {file_path}')
    except yaml.YAMLError as exc:
        raise ConfigError(f'解析错误: {exc}')

    # 结构校验
    if not isinstance(config, dict):
        raise ConfigError('根 错误: 必须是映射')
    generate = config.get('generate')
    if not isinstance(generate, dict):
        raise ConfigError('generate 错误: 必须是映射')
    templates = generate.get('templates')
    if not isinstance(templates, str):
        raise ConfigError('generate.templates 错误: 必须是字符串')
    articles = generate.get('articles')
    if not isinstance(articles, dict):
        raise ConfigError('generate.articles 错误: 必须是映射')
    source = articles.get('source')
    if not isinstance(source, str):
        raise ConfigError('generate.articles.source 错误: 必须是字符串')
    files = articles.get('files')
    if not isinstance(files, list) or not files:
        raise ConfigError('generate.articles.files 错误: 必须是非空序列')
    for file_idx, file_entry in enumerate(files):
        if not isinstance(file_entry, dict):
            raise ConfigError(f'generate.articles.files[{file_idx}] 错误: 必须是映射')
        path = file_entry.get('path')
        if not isinstance(path, str):
            raise ConfigError(f'generate.articles.files[{file_idx}].path 错误: 必须是字符串')
        template = file_entry.get('template')
        if not isinstance(template, str):
            raise ConfigError(f'generate.articles.files[{file_idx}].template 错误: 必须是字符串')

    return config
