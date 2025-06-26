# player_db.py
import json
import os
from ..config import USER_PLAYER_DATA_DIR, USER_PLAYER_DATA_FILE

def _load_players() -> list[dict]:
    """
    加载所有球员数据。如果文件不存在或为空，返回空列表。
    """
    if not os.path.exists(USER_PLAYER_DATA_FILE):
        return []
    try:
        with open(USER_PLAYER_DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content: # 处理文件为空的情况
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        print(f"警告: {USER_PLAYER_DATA_FILE} 文件内容损坏或格式不正确。将初始化为空列表。")
        return [] # 文件损坏时返回空列表
    except Exception as e:
        print(f"加载球员数据时发生错误: {e}")
        return []

def _save_players(players: list[dict]):
    """
    保存所有球员数据到文件。如果目录不存在，则创建。
    """
    os.makedirs(USER_PLAYER_DATA_DIR, exist_ok=True) # 确保数据目录存在
    try:
        with open(USER_PLAYER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(players, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"保存球员数据时发生错误: {e}")

def get_player_by_name(player_name: str) -> dict:
    """
    根据球员姓名检索球员信息。
    Args:
        player_name: 要检索的球员姓名。
    Returns:
        球员信息的字典，如果未找到则返回空字典。
    """
    players = _load_players()
    for player in players:
        if isinstance(player.get("player_name"), str) and player.get("player_name").lower() == player_name.lower(): # type: ignore
            return player
    print(f"未找到球员: {player_name}")
    return {}

def list_all_players() -> list[dict]:
    """
    列出资料库中的所有球员。
    Returns:
        球员字典的列表。
    """
    players = _load_players()
    if not players:
        print("资料库中目前没有球员信息。")
    return players

def add_player(player_data: dict) -> str:
    """
    向资料库添加一个新球员。
    Args:
        player_data: 包含球员信息的字典。
                     期望包含 'player_name' 字段。
    Returns:
        成功添加则返回成功消息，如果球员已存在或数据不完整则返回错误消息。
    """
    player_name = player_data.get("player_name")
    if not player_name or not isinstance(player_name, str):
        return "错误: 添加球员需要提供有效的'player_name'。"

    players = _load_players()
    if any(isinstance(p.get("player_name"), str) and p.get("player_name").lower() == player_name.lower() for p in players): # type: ignore
        return f"错误: 球员 '{player_name}' 已存在于资料库中。"

    players.append(player_data)
    _save_players(players)
    print(f"成功添加球员: {player_name}")
    return f"球员 '{player_name}' 已成功添加到资料库。"

def update_player(player_name: str, updates: dict) -> str:
    """
    更新现有球员的信息。
    Args:
        player_name: 要更新的球员姓名。
        updates: 包含要更新的字段及其新值的字典。
    Returns:
        成功更新则返回成功消息，否则返回错误消息。
    """
    if not player_name or not isinstance(player_name, str):
        return "错误: 更新球员需要提供有效的'player_name'。"
    if not updates:
        return "错误: 更新球员需要提供更新内容。"

    players = _load_players()
    found = False
    for i, player in enumerate(players):
        if isinstance(player.get("player_name"), str) and player.get("player_name").lower() == player_name.lower(): # type: ignore
            players[i].update(updates)
            found = True
            break
    
    if found:
        _save_players(players)
        print(f"成功更新球员: {player_name}")
        return f"球员 '{player_name}' 的信息已成功更新。"
    else:
        return f"错误: 未找到球员 '{player_name}' 进行更新。请检查姓名是否正确。"

def delete_player(player_name: str) -> str:
    """
    从资料库中删除球员。
    Args:
        player_name: 要删除的球员姓名。
    Returns:
        成功删除则返回成功消息，否则返回错误消息。
    """
    if not player_name or not isinstance(player_name, str):
        return "错误: 删除球员需要提供有效的'player_name'。"

    players = _load_players()
    initial_len = len(players)
    players = [p for p in players if not (isinstance(p.get("player_name"), str) and p.get("player_name").lower() == player_name.lower())] # type: ignore
    
    if len(players) < initial_len:
        _save_players(players)
        print(f"成功删除球员: {player_name}")
        return f"球员 '{player_name}' 已成功从资料库中删除。"
    else:
        return f"错误: 未找到球员 '{player_name}' 进行删除。请检查姓名是否正确。"