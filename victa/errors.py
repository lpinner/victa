class VictaError(Exception):
    """ Custom "catchall" Base Exception"""
    pass


class ClassificationError(VictaError, RuntimeError):
    """ Custom Exception raised when classification of a record fails """
    def __init__(self, record, id_field, steps):
        self.record = record
        self.steps = steps

        msg = 'Unable to classify record "{}={}". Visited couplets ("{}")'
        msg = msg.format(id_field,record[id_field], '", "'.join((str(c.id) for c in steps)))
        super(ClassificationError, self).__init__(msg)


class MultipleMatchesError(VictaError, RuntimeError):
    """ Custom Exception raised when multiple rulesets match a record """

    def __init__(self, record, id_field, couplet, rulesets):
        self.record = record
        self.couplet = couplet
        self.rulesets = rulesets

        msg = 'Record "{}={}" matches multiple rulesets for couplet "{}" ("{}")'
        msg = msg.format(id_field,record[id_field], couplet.id, '", "'.join(rulesets))
        super(MultipleMatchesError, self).__init__(msg)


class RuleSyntaxError(VictaError, SyntaxError):
    """ Custom Exception raised when rule parsing fails"""
    pass

