# chatgptとGeminiで作ったから間違っているかも

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("自然数を入力してください。")

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("正の実数を入力してください。")

def get_non_empty_string(prompt):
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            print("空欄は許可されていません。")
        except UnicodeDecodeError:
            print("入力された文字が正しく認識できませんでした。再度入力してください。")

def get_car_costs(num_cars):
    car_costs = []
    payments = {}
    payers = set()  # 支払者の名前を保存するセット
    for i in range(num_cars):
        cost = get_positive_float(f"{i + 1}台目の車の費用を入力してください（円）: ")
        payer = get_non_empty_string(f"{i + 1}台目の費用を支払った人の名前を入力してください: ")
        car_costs.append(cost)
        payments[payer] = payments.get(payer, 0) + cost
        payers.add(payer)
    return car_costs, payments, payers

def get_people_info(num_people, valid_names):
    people = []
    total_days = 0
    while True:
        people.clear()
        total_days = 0
        print("\n--- 車に乗った人の情報を入力してください ---")
        current_people = []

        for i in range(num_people):
            name = get_non_empty_string(f"{i + 1}人目の名前を入力してください: ")
            days = get_positive_float(f"{name}が車を使用した日数(日)を入力してください（0.5日単位）: ")
            current_people.append({"name": name, "days": days})

        # 同乗者の名前の集合
        current_names = set(person["name"] for person in current_people)

        # 支払者が全員同乗しているか確認
        missing_payers = valid_names - current_names
        if missing_payers:
            print("エラー: 以下の支払者が同乗していません。全ての支払者が少なくとも一度は乗っている必要があります。")
            for name in missing_payers:
                print(f" - {name}")
            print("同乗者の入力をやり直してください。")
            continue

        # 問題なければ return
        people = current_people
        for person in people:
            total_days += person["days"]
        return people, total_days

def get_highway_costs(names_set, payments):
    highway_total_costs = {}
    while True:
        use_highway = input("続けて高速料金を入力しますか？（y/n）: ").strip().lower()
        if use_highway == 'n':
            break
        elif use_highway != 'y':
            print("「y」または「n」で入力してください。")
            continue

        while True:  # 高速料金入力のリトライループ
            cost = get_positive_float("高速料金を入力してください（円）: ")
            payer = get_non_empty_string("この高速料金を支払った人の名前を入力してください: ")
            num_riders = get_positive_int("この高速区間を利用した人数(人)を入力してください(支払者を含む): ")

            rider_list = [payer]
            duplicate_found = False

            for i in range(num_riders - 1):
                while True:
                    rider = get_non_empty_string(f"{i + 1}人目の名前を入力してください(支払者を除く): ")
                    if rider == payer:
                        print(f"支払者 '{payer}' は既に利用者リストに含まれています。重複して入力しないでください。")
                        print("\n再度入力してください(この入力以前の高速代の情報は残っています)")
                        duplicate_found = True
                        break  # 内側の while ループを抜けて再入力
                    elif rider not in names_set:
                        print(f"警告: '{rider}' は登録された利用者名ではありません。")
                        print("\n再度入力してください(この入力以前の高速代の情報は残っています)")
                        duplicate_found = True
                        break  # 内側の while ループを抜けて再入力
                    elif rider in rider_list:
                        print(f"'{rider}' はすでにリストに含まれています。")
                        print("\n再度入力してください(この入力以前の高速代の情報は残っています)")
                        duplicate_found = True
                        break  # 内側の while ループを抜けて再入力
                    else:
                        rider_list.append(rider)
                        break  # 正しい入力の場合、内側の while ループを抜ける

                if duplicate_found:
                    break  # 重複があった場合、高速料金入力のリトライループを抜ける

            if not duplicate_found:
                split_cost = cost / len(rider_list)
                for rider in rider_list:
                    highway_total_costs[rider] = highway_total_costs.get(rider, 0) + split_cost
                payments[payer] = payments.get(payer, 0) + cost
                break  # 重複がなければ、高速料金入力のリトライループを抜ける

    return highway_total_costs

from tabulate import tabulate

def display_settlement(people, total_days, total_car_cost, highway_costs, payments):
    print("\n================ 精算結果 ================\n")

    table_data = []
    total_due_sum_displayed = 0
    total_paid_sum_displayed = 0
    individual_balances = {}
    epsilon = 1e-2

    for person in people:
        name = person["name"]
        days = person["days"]
        share = days / total_days if total_days > 0 else 0
        car_due = share * total_car_cost
        highway_due = highway_costs.get(name, 0)
        total_due = car_due + highway_due
        paid = payments.get(name, 0)
        balance = paid - total_due
        individual_balances[name] = balance

        table_data.append([
            name, f"{days:.1f}", f"{car_due:.3f}", f"{highway_due:.3f}",
            f"{total_due:.3f}", f"{paid:.3f}", f"{balance:.3f}"
        ])
        total_due_sum_displayed += total_due
        total_paid_sum_displayed += paid

    headers = ["氏名", "日数", "車(円)", "高速(円)", "合計(円)", "支払(円)", "差額"]
    colalign = ("center", "right", "right", "right", "right", "right", "right")
    print(tabulate(table_data, headers=headers, tablefmt="simple", stralign="center", numalign="right", colalign=colalign))

    # 検算処理 (表示された合計金額を使用)
    if abs(total_due_sum_displayed - total_paid_sum_displayed) > epsilon:
        print("\n[エラー] 請求額の合計と支払額の合計が一致しません。")
        print(f"請求額の合計: {total_due_sum_displayed:.2f} 円")
        print(f"支払額の合計: {total_paid_sum_displayed:.2f} 円")
    else:
        print("\n検算OK：請求額の合計と支払額の合計は一致しています。\n")

    # LINE送信用出力
    print("\n================ LINE送信用メッセージ ================\n")
    for person in people:
        name = person["name"]
        share = person["days"] / total_days if total_days > 0 else 0
        car_due = share * total_car_cost
        highway_due = highway_costs.get(name, 0)
        total_due = car_due + highway_due
        paid = payments.get(name, 0)
        balance = paid - total_due

        if abs(balance) < epsilon:
            continue

        sign = "+" if balance > 0 else "-"
        print(f"{name}: {sign}{abs(balance):.1f} 円")

def main():
    num_cars = get_positive_int("使用した車の台数を入力してください(台): ")
    car_costs, payments, car_payers = get_car_costs(num_cars)
    total_car_cost = sum(car_costs)
    print(f"\n車代の合計: {total_car_cost:.0f} 円\n")

    num_people = get_positive_int("車に乗った人数を入力してください(人): ")
    people, total_days = get_people_info(num_people, car_payers)

    names_set = set(person["name"] for person in people)

    highway_costs = get_highway_costs(names_set, payments)

    display_settlement(people, total_days, total_car_cost, highway_costs, payments)


if __name__ == "__main__":
    main()