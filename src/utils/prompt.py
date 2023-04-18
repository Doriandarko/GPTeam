from enum import Enum
from langchain.schema import SystemMessage, BaseMessage
from pydantic import BaseModel


class PromptString(Enum):
    REFLECTION_QUESTIONS = "Here are a list of statements:\n{memory_descriptions}\n\nGiven only the information above, what are 3 most salient high-level questions we can answer about the subjects in the statements?\n\n{format_instructions}"

    REFLECTION_INSIGHTS = "\n{memory_strings}\nWhat 5 high-level insights can you infer from the above statements?\nWhen referring to people, always specify their full name.\n\n{format_instructions}"

    IMPORTANCE = "You are a memory importance AI. Given the character's profile and the memory description, rate the importance of the memory on a scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance). Be sure to make your rating relative to the character's personality and concerns.\n\nExample #1:\nName: Jojo\nBio: Jojo is a professional ice-skater who loves specialty coffee. She hopes to compete in the olympics one day.\nMemory: Jojo sees a new coffee shop\n\n Your Response: '{{\"rating\": 3}}'\n\nExample #2:\nName: Skylar\nBio: Skylar is a product marketing manager. She works at a growth-stage tech company that makes autonomous cars. She loves cats.\nMemory: Skylar sees a new coffee shop\n\n Your Response: '{{\"rating\": 1}}'\n\nExample #3:\nName: Bob\nBio: Bob is a plumber living in the lower east side of New York City. He's been working as a plumber for 20 years. On the weekends he enjoys taking long walks with his wife. \nMemory: Bob's wife slaps him in the face.\n\n Your Response: '{{\"rating\": 9}}'\n\nExample #4:\nName: Thomas\nBio: Thomas is a police officer in Minneapolis. He joined the force only 6 months ago, and having a hard time at work because of his inexperience.\nMemory: Thomas accidentally spills his drink on a stranger\n\n Your Response: '{{\"rating\": 6}}'\n\n{format_instructions} Let's Begin! \n\n Name: {full_name}\nBio: {bio}\nMemory:{memory_description}\n\n"

    RECENT_ACTIIVITY = "Given the following memories, generate a short summary of what {full_name} has been doing lately. Do not make up details that are not specified in the memories. \n\nMemories: {memory_descriptions}"

    MAKE_PLANS = 'You are a plan generating AI. Given the character\'s bio, goals, recent activity, and current plans, generate additional plans for them to carry out, such that the final set of plans include at least {time_window} of activity. The plan list should be numbered, with each plan containing a description, location, start time, stop condition, and max duration.\n\nExample Plan: \'{{"index": 1, "description": "Cook dinner", "location": "Jane\'s Kitchen","start_time": "20:00 - 12/12/22","max_duration_hrs": 1.5, "stop_condition": "Dinner is fully prepared"}}\'\n\nFor each plan, pick the most reasonable location out of this list: {location_descriptions}\n\n{format_instructions}\n\nLet\'s Begin!\n\nName: {full_name}\nBio: {bio}\nGoals: {directives}\nRecent Activity: {recent_activity}\nCurrent Plans: {current_plans}'

    EXECUTE_PLAN = "Given the tools, complete the task as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nTask: the task you must complete\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: 'I have completed the task'\nFinal Response: the final response to the task\n\nIf you determine that you are incapable of completing the task with the tools you have been given, return 'Final Response: Task Failed'\nBegin!\n\nTask: {input}\n\n{agent_scratchpad}"

    REACT = (
        "You are a reaction AI. Given the character's personal info and current plans, decide whether they should continue with their current plans, or if they should make new plans based on the new events. If the events have a material impact on the character's goals or existing plans, they should always make new plans.\n\n{format_instructions}\n\nLet's Being!\n\nName: {full_name}\nBio: {bio}\nGoals: {directives}\nRecent Activity: {recent_activity}\nCurrent Plans: {current_plans}\n\nNew Events: {event_descriptions}."
    )

class Prompter(BaseModel):
    template: str
    inputs: dict

    def __init__(self, template: PromptString, inputs: dict) -> None:
        super().__init__(inputs=inputs, template=template.value)

    @property
    def prompt(self) -> list[BaseMessage]:
        final_string = self.template.format(**self.inputs)
        messages = [SystemMessage(content=final_string)]
        return messages