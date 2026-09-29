"""第01回の読む比較。受付候補をPythonの反復で列挙する。"""
available = [("aki", "tue"), ("aki", "wed"), ("ben", "tue"), ("chi", "wed")]
trained = [("aki", "register"), ("aki", "repair"),
           ("ben", "register"), ("chi", "repair")]

for person, day in available:
    if (person, "register") in trained:
        print(person, day)
