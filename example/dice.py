import random
import re

from nonebot import on_command
from nonebot.adapters.telegram import Bot, Event


@on_command("r").handle()
async def _(bot: Bot, event: Event):
    await bot.send(event, Calculator(str(event.get_message())).run())


class DiceException(Exception):
    pass


class Calculator:
    def __init__(self, expression: str, default_dice: int = 100):
        self.expression = expression
        self.source = expression
        self.detail = expression
        self.default_dice = default_dice

    def __add__(self, other: "Calculator") -> "Calculator":
        result = self.new(self.expression + "+" + other.expression)
        result.source = self.source + "+" + other.source
        result.detail = self.detail + "+" + other.detail
        result.result = self.result + other.result
        return result

    def __sub__(self, other: "Calculator") -> "Calculator":
        result = self.new(self.expression + "-" + other.expression)
        result.source = self.source + "-" + other.source
        result.detail = self.detail + "-" + other.detail
        result.result = self.result - other.result
        return result

    def __mul__(self, other: "Calculator") -> "Calculator":
        result = self.new(self.expression + "*" + other.expression)
        result.source = self.source + "*" + other.source
        result.detail = self.detail + "*" + other.detail
        result.result = self.result * other.result
        return result

    def __truediv__(self, other: "Calculator") -> "Calculator":
        result = self.new(self.expression + "/" + other.expression)
        result.source = self.source + "/" + other.source
        result.detail = self.detail + "/" + other.detail
        result.result = self.result / other.result
        return result

    def __pow__(self, other: "Calculator") -> "Calculator":
        result = self.new(self.expression + "^" + other.expression)
        result.source = self.source + "^" + other.source
        result.detail = self.detail + "^" + other.detail
        result.result = self.result ** other.result
        return result

    def __str__(self):
        return f"{self.source}{' = ' + self.detail if self.show_detail else ''} = {int(self.result)}"

    @classmethod
    def new(cls, expression: str, default_dice: int = 100) -> "Calculator":
        return cls(expression, default_dice)

    def run(self, show_detail: bool = True) -> str:
        self.show_detail = show_detail
        result = ""
        self._extract_roundnum_and_reason()
        for i in range(self.round_num):
            self.expression = self.source
            self._calculate_with_bracket()
            result += "\n" + str(self)
        return result

    def calculate(self) -> int:
        self.expression = self.expression.upper()
        self._calculate_with_bracket()
        return int(self.result)

    # 提取轮数和原因
    def _extract_roundnum_and_reason(self):
        # 匹配正则
        match_result = re.search(r"((\d*)#)?([dDkK\d.+\-*/^()]*)(.*)", self.expression)

        # 获取轮数，获取不到默认为1
        round_num = match_result.group(2)
        self.round_num = int(round_num) if round_num else 1

        if self.round_num <= 0 or self.round_num > 10:
            raise DiceException("非法轮数")

        # 获取表达式
        self.source = match_result.group(3).upper()

        # 获取掷骰原因
        self.reason = match_result.group(4).strip()

    # 计算有括号的表达式
    def _calculate_with_bracket(self):
        expression = self.expression
        right_bracket_position = expression.find(")")
        if right_bracket_position >= 0:
            expression_in_left = expression[:right_bracket_position]
            expression_in_right = expression[right_bracket_position + 1 :]
            left_bracket_position = expression_in_left.rfind("(")
            if left_bracket_position >= 0:
                calculator_in_bracket = self.new(
                    expression=expression_in_left[left_bracket_position + 1 :],
                )
                calculator_in_bracket._calculate_without_bracket()
                expression_in_left = expression_in_left[:left_bracket_position]
                self.source = (
                    expression_in_left
                    + "("
                    + calculator_in_bracket.source
                    + ")"
                    + expression_in_right
                )
                self.expression = (
                    expression_in_left
                    + str(int(calculator_in_bracket.result))
                    + expression_in_right
                )
                self.detail = (
                    expression_in_left
                    + "("
                    + calculator_in_bracket.detail
                    + ")"
                    + expression_in_right
                )
                self._calculate_with_bracket()
            else:
                self._calculate_without_bracket()
        else:
            self._calculate_without_bracket()

    # 计算无括号的表达式
    def _calculate_without_bracket(self):

        # 去除无效括号
        self.expression = self.expression.replace("(", "").replace(")", "")

        if re.search(r"[+\-*/^]", self.expression):
            if "+" in self.expression:
                operator = "+"
                operator_position = self.expression.find("+")
            elif "-" in self.expression:
                operator = "-"
                operator_position = self.expression.find("-")
            elif "*" in self.expression:
                operator = "*"
                operator_position = self.expression.find("*")
            elif "/" in self.expression:
                operator = "/"
                operator_position = self.expression.find("/")
            elif "^" in self.expression:
                operator = "^"
                operator_position = self.expression.find("^")

            calculator_in_left = self.new(self.expression[:operator_position])
            calculator_in_right = self.new(self.expression[operator_position + 1 :])

            if calculator_in_left.expression and calculator_in_right.expression:
                calculator_in_left._calculate_without_bracket()
                calculator_in_right._calculate_without_bracket()
                if operator == "+":
                    calculator_result = calculator_in_left + calculator_in_right
                elif operator == "-":
                    calculator_result = calculator_in_left - calculator_in_right
                elif operator == "*":
                    calculator_result = calculator_in_left * calculator_in_right
                elif operator == "/":
                    calculator_result = calculator_in_left / calculator_in_right
                elif operator == "^":
                    calculator_result = calculator_in_left ** calculator_in_right
            else:
                if calculator_in_left.expression:
                    calculator_result = calculator_in_right
                elif calculator_in_right.expression:
                    calculator_result = calculator_in_left

                calculator_result._calculate_without_bracket()

            self.expression = calculator_result.expression
            self.detail = calculator_result.detail
            self.result = calculator_result.result
        elif re.search(r"(\d*)D(\d*)(K(\d*))?", self.expression):
            self._throw_dice()
        else:
            self.result = float(self.expression)

    # 掷骰
    def _throw_dice(self):
        expression = self.expression
        default_dice = self.default_dice

        # 匹配正则
        match_result = re.search(r"(\d*)D(\d*)(K(\d*))?(.*)", expression)

        # 获取骰数，获取不到默认为1，超过100或等于0报错
        dice_num = match_result.group(1)
        dice_num = int(dice_num) if dice_num else 1

        if dice_num <= 0 or dice_num > 100:
            raise DiceException("非法骰数")

        # 获取骰面，获取不到默认为100，超过1000或等于0报错
        dice_face = match_result.group(2)
        dice_face = int(dice_face) if dice_face else default_dice

        if dice_face <= 0 or dice_face > 1000:
            raise DiceException("非法骰面")

        # 获取有效骰数，获取不到默认为骰数，超过骰数或等于0报错
        dice_pick = match_result.group(4)
        dice_pick = int(dice_pick) if dice_pick else dice_num

        if dice_pick <= 0 or dice_pick > dice_num:
            raise DiceException("非法有效骰数")

        # 排除错误表达式
        if match_result.group(5):
            raise DiceException("非法表达式")

        # 模拟现实掷骰
        dice_result_list = []
        for i in range(dice_num):
            dice_result = random.randint(1, dice_face)
            dice_result_list.append(dice_result)

        # 降序排列，为计算有效骰作准备
        dice_result_list.sort(reverse=True)

        # 统计骰子以及还原计算过程
        self.detail = "["
        dice_count = 0.0
        for i in range(dice_num):
            if i:
                self.detail += "+"
            if i < dice_pick:
                self.detail += str(dice_result_list[i])
                dice_count += dice_result_list[i]
            else:
                self.detail += "(" + str(dice_result_list[i]) + ")"
        self.detail += "]"
        self.result = dice_count


# 测试用
if __name__ == "__main__":
    while True:
        print(Calculator(input()).run())
