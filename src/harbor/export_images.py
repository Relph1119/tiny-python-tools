#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: export_images.py
@time: 2024/9/24 4:22
@project: tiny-python-tools
@desc: 导出Harbor中的所有镜像
"""
import datetime
import json
import logging
import os
import subprocess
from os import path

# 配置日志
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
log_filename = f'export_images-{current_date}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 替换这里的Harbor仓库地址和凭据
harbor_url = "https://abc.com.cn"
harbor_name = "abc.com.cn"
username = "admin"
password = "admin"
Tar_File = "/data/Harbor-backup_new"

if not os.path.exists(Tar_File):
    os.mkdir(Tar_File)

# 执行Curl命令获取项目列表
try:
    curl_output = subprocess.check_output(
        f'curl --insecure -u "{username}:{password}" -X GET -H "Content-Type: application/json" {harbor_url}/api/v2.0/projects|python -m json.tool',
        shell=True
    ).decode('utf-8')
except subprocess.CalledProcessError as e:
    logging.error(f"获取项目列表时出错: {e}")
    exit(1)

# 将Curl命令的输出解析为JSON
try:
    projects = json.loads(curl_output)
except json.JSONDecodeError as e:
    logging.error(f"无法解析JSON数据: {e}")
    exit(1)

# 遍历项目列表
for project in projects:
    project_name = project["name"]
    project_repo_count = project['repo_count']
    project_path = path.join(Tar_File, project_name)
    if not os.path.exists(project_path):
        os.mkdir(project_path)

    i = 0
    if i * 100 < project_repo_count:
        next_i = i + 1
        # 执行Curl命令获取项目下的镜像列表
        try:
            curl_output = subprocess.check_output(
                f'curl --insecure -u "{username}:{password}" -X GET -H "Content-Type: application/json" "{harbor_url}/api/v2.0/projects/{project_name}/repositories?page={next_i}&page_size=100" | python -m json.tool',
                shell=True
            ).decode('utf-8')
        except subprocess.CalledProcessError as e:
            logging.error(f"获取项目 {project_name} 的镜像列表时出错: {e}")
            continue

        # 将Curl命令的输出解析为JSON
        try:
            repositories = json.loads(curl_output)
        except json.JSONDecodeError as e:
            logging.error(f"无法解析项目 {project_name} 的镜像列表: {e}")
            continue

        # 遍历镜像列表
        for repo in repositories:
            repo_name = repo["name"]
            repo_name_new_repo_name = repo_name.split("/", 1)
            if len(repo_name_new_repo_name) > 1:
                # 如果成功分割出两部分，repo_name_new_repo_name[1] 将包含第一个斜杠之后的部分
                new_repo_name = repo_name_new_repo_name[1]
            else:
                # 如果没有斜杠或只有一个斜杠，将保持原始 repo_name
                new_repo_name = repo_name

            # 执行Curl命令获取镜像标签列表
            try:
                curl_output = subprocess.check_output(
                    f'curl --insecure -u "{username}:{password}" -X GET -H "Content-Type: application/json" {harbor_url}/api/v2.0/projects/{project_name}/repositories/{new_repo_name}/artifacts?page_size=100',
                    shell=True
                ).decode('utf-8')
            except subprocess.CalledProcessError as e:
                logging.error(f"获取镜像 {repo_name} 标签列表时出错: {e}")
                continue

            # 提取标签信息
            try:
                artifacts = json.loads(curl_output)
                for image_info in artifacts:
                    digest = image_info.get('name')
                    tags = image_info.get('tags')
                    # 遍历每个标签并构建镜像地址
                    if tags is not None and digest is not None:
                        for tag in tags:
                            tag_name = tag["name"]
                            source_image_url = f"{harbor_name}/{project_name}/{new_repo_name}:{tag_name}"

                            # 拉取源镜像
                            try:
                                subprocess.check_call(
                                    f'docker pull {source_image_url}',
                                    shell=True
                                )
                            except subprocess.CalledProcessError as e:
                                logging.error(f"无法拉取镜像 {source_image_url}: {e}")
                                continue

                            # 保存镜像到本地
                            image_save_path = path.join(project_path, new_repo_name + "." + tag_name + ".tar.gz")
                            try:
                                subprocess.check_call(
                                    f'docker save {source_image_url} | gzip > {image_save_path}',
                                    shell=True
                                )
                            except subprocess.CalledProcessError as e:
                                logging.error(f"无法拉取镜像 {source_image_url}: {e}")
                                continue

                            # 删除本地源镜像
                            try:
                                subprocess.check_call(
                                    f'docker rmi {source_image_url}',
                                    shell=True
                                )
                            except subprocess.CalledProcessError as e:
                                logging.error(f"无法删除本地镜像 {source_image_url}: {e}")
                                continue

            except json.JSONDecodeError as e:
                logging.error(f"无法解析镜像 {repo_name} 的标签信息: {e}")
                continue
        i = next_i

logging.info("镜像复制完成。")
