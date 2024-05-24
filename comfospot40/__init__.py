from comfospot40.packet import Packet
from comfospot40.value import Value
from comfospot40.temperature import Temperature
from comfospot40.humidity import Humidity
from comfospot40.fanspeed import Fanspeed
from comfospot40.zone import Zone
from comfospot40.state import State
from comfospot40.parser import Parser
from comfospot40.create_packet import create_speed_packet
from comfospot40.mqtt import Mqtt
from comfospot40.hal import Hal
from comfospot40.counterfan import Counterfan

# Keep ruff happy
assert Packet
assert Value
assert Temperature
assert Humidity
assert Fanspeed
assert Zone
assert State
assert Parser
assert create_speed_packet
assert Mqtt
assert Hal
assert Counterfan
