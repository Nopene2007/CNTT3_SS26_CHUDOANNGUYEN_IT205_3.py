from abc import ABC, abstractmethod
class Champion(ABC):
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int):
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp if base_hp > 0 else 100
        self.base_atk = base_atk if base_atk > 0 else 100
    @abstractmethod
    def calculate_skill_damage(self) -> float:
        pass
    def get_combat_power(self) -> float:
        return self.base_hp + (self.calculate_skill_damage() * 1.5)
    def __add__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        elif isinstance(other, (int, float)):
            return self.get_combat_power() + other
        return NotImplemented
    def __radd__(self, other):
        return self.__add__(other)
    def __gt__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() > other.get_combat_power()
        return NotImplemented
class Warrior(Champion):
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, shield_bonus: int):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.shield_bonus = shield_bonus if shield_bonus >= 0 else 0
    def calculate_skill_damage(self) -> float:
        return (self.base_atk * 2) + self.shield_bonus
class Mage(Champion):
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, ability_power: float):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.ability_power = ability_power if ability_power > 0 else 1.0
    def calculate_skill_damage(self) -> float:
        return self.base_atk * self.ability_power
class GameSystem:
    def __init__(self):
        self.champion_pool = {
            "WAR01": Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
            "WAR02": Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
            "MAG01": Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5)
        }
    def display_pool(self):
        print(f"{'Mã':<6} | {'Tên tướng':<18} | {'Hệ':<8} | {'HP':<5} | {'ATK':<5} | {'Chỉ số riêng':<15} | {'Chiến lực'}")
        for champion in self.champion_pool.values():
            form = "Warrior" if isinstance(champion, Warrior) else "Mage"
            chi_so_rieng = f"Armor: {champion.shield_bonus}" if isinstance(champion, Warrior) else f"AP: {champion.ability_power}"
            print(f"{champion.champion_id:<6} | {champion.name:<18} | {form:<8} | {champion.base_hp:<5} | {champion.base_atk:<5} | {chi_so_rieng:<15} | {champion.get_combat_power():.0f}")
    def add_champion(self):
        champion_id = input("Nhập mã tướng: ").strip().upper()
        if champion_id in self.champion_pool:
            print("Mã tướng đã tồn tại trong bể tướng!")
            return
        print("Chọn hệ tộc: 1 - Warrior | 2 - Mage")
        choice = input("Lựa chọn: ").strip()
        if choice not in ["1", "2"]:
            print("Lựa chọn hệ tộc không hợp lệ!")
            return
        name=input("Nhập tên tướng: ").strip()
        try:
            hp=int(input("Nhập HP: "))
            atk=int(input("Nhập ATK: "))
            if choice == "1":
                armor = int(input("Nhập Armor (Shield Bonus): "))
                new_champ = Warrior(champion_id, name, hp, atk, armor)
                he_name = "Warrior"
            else:
                ap = float(input("Nhập Hệ số phép thuật (AP): "))
                new_champ = Mage(champion_id, name, hp, atk, ap)
                he_name = "Mage"
            self.champion_pool[champion_id] = new_champ
            print(f"Thêm tướng {he_name} thành công!")
            print(f"Mã: {new_champ.champion_id} | Tên: {new_champ.name} | Chiến lực: {new_champ.get_combat_power():.0f}")
        except ValueError:
            print("Các chỉ số HP, ATK, Thuộc tính riêng phải là số!")
    def compare_champions(self):
        id_1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
        id_2 = input("Nhập mã tướng thứ hai: ").strip().upper()
        if id_1 not in self.champion_pool or id_2 not in self.champion_pool:
            print("Một hoặc cả hai mã tướng không tồn tại trong hệ thống!")
            return
        cham_1 = self.champion_pool[id_1]
        cham_2 = self.champion_pool[id_2]
        print(f"{cham_1.champion_id} - {cham_1.name} | Hệ: {'Warrior' if isinstance(cham_1, Warrior) else 'Mage'} | Chiến lực: {cham_1.get_combat_power():.0f}")
        print(f"{cham_2.champion_id} - {cham_2.name} | Hệ: {'Warrior' if isinstance(cham_2, Warrior) else 'Mage'} | Chiến lực: {cham_2.get_combat_power():.0f}")
        if cham_1 > cham_2:
            print(f"Kết quả: {cham_1.champion_id} - {cham_1.name} mạnh hơn {cham_2.champion_id} - {cham_2.name}.")
        elif cham_2 > cham_1:
            print(f"Kết quả: {cham_2.champion_id} - {cham_2.name} mạnh hơn {cham_1.champion_id} - {cham_1.name}.")
        else:
            print("Kết quả: Hai quân cờ có chiến lực ngang nhau.")
    def calculate_team_power(self):
        raw_input = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
        input_ids = [i.strip().upper() for i in raw_input.split(",") if i.strip()]
        team_list = []
        print("Danh sách đội hình:")
        stt = 1
        for champion in input_ids:
            if champion not in self.champion_pool:
                print(f"Mã tướng [{champion}] không hợp lệ, bỏ qua!")
                continue
            champ = self.champion_pool[champion]
            print(f"{stt}. {champ.champion_id} - {champ.name} | Chiến lực: {champ.get_combat_power():.0f}")
            team_list.append(champ)
            stt += 1
        if not team_list:
            print("Đội hình rỗng hoặc không có tướng nào hợp lệ!")
            return
        total_power = sum(team_list)
        print(f"Tổng chiến lực đội hình: {total_power:.0f}")
    def run(self):
        try:
            champion= Champion("ERROR", "Ghost", 100, 100)
        except TypeError:
            print("[Hệ thống] Bảo mật OK: Lớp trừu tượng Champion đã được bảo vệ, cấm khởi tạo trực tiếp!")
        while True:
            print("================ RIKKEI RPG MENU ================")
            print("1. Hiển thị bể tướng hiện có")
            print("2. Thêm quân cờ mới")
            print("3. So sánh 2 quân cờ")
            print("4. Tính tổng chiến lực Đội Hình Ra Sân")
            print("5. Thoát chương trình")
            choice = input("Chọn chức năng (1-5): ").strip()
            if choice == "1": self.display_pool()
            elif choice == "2": self.add_champion()
            elif choice == "3": self.compare_champions()
            elif choice == "4": self.calculate_team_power()
            elif choice == "5":
                print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
                break
            else:
                print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 5.")
if __name__ == "__main__":
    system = GameSystem()
    system.run()