﻿namespace KbUtil.Lib.Deserialization
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Xml.Linq;
    using KbUtil.Lib.Models.Keyboard;

    public class KeyboardDataDeserializer
    {
        public static Keyboard Deserialize(XElement xElement)
        {
            var keyboard = new Keyboard();

            DeserializeGroup(xElement, keyboard);

            if(TryGetAttribute(xElement, "Version", out XAttribute versionAttribute))
            {
                keyboard.Version = versionAttribute.ValueAsVersion();
            }

            return keyboard;
        }

        private static void DeserializeKey(XElement keyElement, Key key)
        {
            DeserializeElement(keyElement, key);

            IEnumerable<XElement> legendElements = keyElement
                .Nodes()
                .Where(node =>
                    node.NodeType == System.Xml.XmlNodeType.Element
                    && ((XElement)node).Name == "Legend")
                .Select(node => (XElement)node);

            var legends = new List<Legend>();
            foreach (var legendElement in legendElements)
            {
                legends.Add(DeserializeLegend(legendElement));
            }
            key.Legends = legends;
        }

        private static Legend DeserializeLegend(XElement legendElement)
        {
            var legend = new Legend();

            if(TryGetAttribute(legendElement, "HorizontalAlignment", out XAttribute horizontalAlignmentAttribute))
            {
                legend.HorizontalAlignment = horizontalAlignmentAttribute.ValueAsLegendHorizontalAlignment();
            }

            if(TryGetAttribute(legendElement, "VerticalAlignment", out XAttribute verticalAlignmentAttribute))
            {
                legend.VerticalAlignment = verticalAlignmentAttribute.ValueAsLegendVerticalAlignment();
            }

            if(TryGetAttribute(legendElement, "Text", out XAttribute textAttribute))
            {
                legend.Text = textAttribute.ValueAsString();
            }

            if(TryGetAttribute(legendElement, "FontSize", out XAttribute fontSizeAttribute))
            {
                legend.FontSize = fontSizeAttribute.ValueAsFloat();
            }

            return legend;
        }

        private static void DeserializeStack(XElement xElement, Stack stack)
        {
            DeserializeGroup(xElement, stack);

            if(TryGetAttribute(xElement, "Orientation", out XAttribute orientationAttribute))
            {
                stack.Orientation = orientationAttribute.ValueAsStackOrientation();
            }
        }

        private static void DeserializeGroup(XElement xElement, Group group)
        {
            DeserializeElement(xElement, group);

            IEnumerable<XElement> childElements = xElement
                .Nodes()
                .Where(node =>
                    node.NodeType == System.Xml.XmlNodeType.Element)
                .Select(node => (XElement)node);

            List<Element> children = childElements
                .Select(childElement => DeserializeChild(group, childElement))
                .ToList();

            group.Children = children;
        }

        private static Element DeserializeChild(Element parent, XElement childElement)
        {
            Element child;

            switch (childElement.Name.ToString())
            {
                case "Stack":
                    child = new Stack { Parent = parent };
                    DeserializeStack(childElement, (Stack)child);
                    break;
                case "Group":
                    child = new Group { Parent = parent };
                    DeserializeGroup(childElement, (Group)child);
                    break;
                case "Key":
                    child = new Key { Parent = parent };
                    DeserializeKey(childElement, (Key)child);
                    break;
                default:
                    throw new Exception();
            }
            return child;
        }

        private static void DeserializeElement(XElement xElement, Element element)
        {
            if(TryGetAttribute(xElement, "Name", out XAttribute nameAttribute))
            {
                element.Name = nameAttribute.ValueAsString();
            }

            if(TryGetAttribute(xElement, "XOffset", out XAttribute xOffsetAttribute))
            {
                element.XOffset = xOffsetAttribute.ValueAsFloat();
            }

            if(TryGetAttribute(xElement, "YOffset", out XAttribute yOffsetAttribute))
            {
                element.YOffset = yOffsetAttribute.ValueAsFloat();
            }

            if(TryGetAttribute(xElement, "Rotation", out XAttribute rotationAttribute))
            {
                element.Rotation = rotationAttribute.ValueAsFloat();
            }

            if(TryGetAttribute(xElement, "Height", out XAttribute heightAttribute))
            {
                // This is a bit hacky but it's easier to set key dimensions via units instead of mm
                string heightString = heightAttribute.ValueAsString();
                if (heightString.EndsWith("u"))
                {
                    element.Height = float.Parse(heightString.Replace("u", string.Empty)) * Constants.KeyDiameterMillimeters1u;
                }
                else
                {
                    element.Height = heightAttribute.ValueAsFloat();
                }
            }

            if(TryGetAttribute(xElement, "Width", out XAttribute widthAttribute))
            {
                // This is a bit hacky but it's easier to set key dimensions via units instead of mm
                string widthString = widthAttribute.ValueAsString();
                if (widthString.EndsWith("u"))
                {
                    element.Width = float.Parse(widthString.Replace("u", string.Empty)) * Constants.KeyDiameterMillimeters1u;
                }
                else
                {
                    element.Width = widthAttribute.ValueAsFloat();
                }
            }

            if(TryGetAttribute(xElement, "Margin", out XAttribute marginAttribute))
            {
                element.Margin = marginAttribute.ValueAsFloat();
            }

            if(TryGetAttribute(xElement, "Debug", out XAttribute debugAttribute))
            {
                element.Debug = debugAttribute.ValueAsBool();
            }
        }

        private static bool TryGetAttribute(XElement xElement, string attributeName, out XAttribute attribute)
        {
            if (xElement == null || string.IsNullOrWhiteSpace(attributeName))
            {
                attribute = null;
                return false;
            }

            attribute = xElement
                .Attributes()
                .FirstOrDefault(attr => attr.Name.ToString() == attributeName);

            return !(attribute is default);
        }
    }
}